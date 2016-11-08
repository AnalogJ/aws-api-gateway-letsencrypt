#!/usr/bin/env python
import subprocess, os
import sys, json, datetime
import glob
import distutils.spawn

###############################################################################
# The script below expects the following environmental variables to be defined:
# - DOMAIN
# - API_GATEWAY_NAME
# - PROVIDER (defaults to 'cloudflare')
# - LEXICON_*_USERNAME & LEXICON_*_TOKEN
#
# When provided with the correct environmental variables it will do the following:
# - validate that the specified AWS API Gateway exists
# - generate a new set of letsencrypt certificates for the specified Domain
# - register custom domain name with AWS (and create a distribution domain name)
# - add a CNAME dns record mapping your custom domain to AWS distribution domain
# - map custom domain to API Gateway name
#
# Nothing below this line should be changed.
###############################################################################
print '--> Validating that all required executables are available on the PATH'
if not distutils.spawn.find_executable('lexicon'): raise StandardError('lexicon executable is not available on the path')
if not distutils.spawn.find_executable('aws'): raise StandardError('aws cli is not available on the path')
if not distutils.spawn.find_executable('dehydrated'): raise StandardError('dehydrated executable is not available on the path')

print '--> Validating that all required environmental variables are set'
if 'DOMAIN' not in os.environ: raise StandardError('DOMAIN environmental variable must be specified.')
if 'API_GATEWAY_NAME' not in os.environ: raise StandardError('API_GATEWAY_NAME environmental variable must be specified.')
if 'AWS_ACCESS_KEY_ID' not in os.environ: raise StandardError('AWS_ACCESS_KEY_ID environmental variable must be specified')
if 'AWS_SECRET_ACCESS_KEY' not in os.environ: raise StandardError('AWS_ACCESS_KEY_ID environmental variable must be specified')

os.environ['PROVIDER'] = os.environ.get('PROVIDER', 'cloudflare')
os.environ['AWS_DEFAULT_REGION'] = os.environ.get('AWS_DEFAULT_REGION','us-east-1')
os.environ['CLEANUP'] = os.environ.get('CLEANUP','true')

# Lexicon environmental variables
lexicon_provider_username_env = "LEXICON_{0}_USERNAME".format(os.environ['PROVIDER'].upper())
lexicon_provider_token_env = "LEXICON_{0}_TOKEN".format(os.environ['PROVIDER'].upper())

if lexicon_provider_username_env not in os.environ: raise StandardError('{0} environmental variable must be specified'.format(lexicon_provider_username_env))
if lexicon_provider_token_env not in os.environ: raise StandardError('{0} environmental variable must be specified'.format(lexicon_provider_token_env))
cust_env = os.environ.copy()

print "--> Ensure that our API Gateway exists (otherwise none of this matters)"
api_gateway_cmd = ['aws', 'apigateway', 'get-rest-apis', '--query',
                   'items[?name==`{0}`] | [0].id'.format(cust_env['API_GATEWAY_NAME'])
                   ]
api_gateway_id = json.loads(subprocess.check_output(api_gateway_cmd))

if not api_gateway_id:
    print "API Gateway does not exist!"
    sys.exit(-1)



print "--> Configure Dehydrated & Lexicon (keysize for AWS has to be 2048)"
with open('config/dehydrated_config.txt','w+') as f:
    f.write('KEYSIZE="2048"')

print "--> Generating letsencrypt SSL Certificates for '{0}'".format(cust_env['DOMAIN'])
subprocess.call([
    'dehydrated',
    '--config', 'config/dehydrated_config.txt',
    '--domain', cust_env['DOMAIN'],
    '--cron',
    '--out', 'certs',
    '--hook', 'config/dehydrated.hook.sh',
    '--challenge', 'dns-01'
], env=cust_env)



print "--> Check if '{0}' is already registered with AWS api gateway".format(cust_env['DOMAIN'])
dist_domain_name_cmd = [
    'aws', 'apigateway', 'get-domain-name', '--domain-name', cust_env['DOMAIN'],
    '--query', 'distributionDomainName'
]
dist_domain_name = None

try:
    dist_domain_name = json.loads(subprocess.check_output(dist_domain_name_cmd))
    print 'Successfully retrieved existing AWS distribution domain name'
    #TODO: we should update the existing certificates with the new ones here, but the cli doesnt seem to support that yet.
    # https://www.reddit.com/r/aws/comments/4pypkm/updating_an_api_gateway_ssl_certificate_with_the/
except:
    print 'Registering domain with AWS api gateway'

    with open('certs/{0}/cert.pem'.format(cust_env['DOMAIN']),'r+') as cert_file, open('certs/{0}/privkey.pem'.format(cust_env['DOMAIN']),'r+') as privkey_file, open('certs/{0}/chain.pem'.format(cust_env['DOMAIN']),'r+') as chain_file:
        dist_domain_name_cmd = [
            'aws', 'apigateway', 'create-domain-name',
            '--domain-name', cust_env['DOMAIN'],
            '--certificate-name', "lexicon-{0}".format(date.isoformat()),
            '--certificate-body', cert_file.read(),
            '--certificate-private-key', privkey_file.read(),
            '--certificate-chain', chain_file.read(),
            '--query', 'distributionDomainName'
        ]
        dist_domain_name = json.loads(subprocess.check_output(dist_domain_name_cmd))



print "--> Create or update CNAME DNS record for {0} which points to AWS distribution domain name".format(cust_env['PROVIDER'])
subprocess.Popen([
    'lexicon', cust_env['PROVIDER'], 'create', cust_env['DOMAIN'], 'CNAME',
    '--name={0}'.format(cust_env['DOMAIN']),
    '--content={0}'.format(dist_domain_name)
], env=cust_env)



print "--> Check if custom domain is already mapped to API Gateway"
base_path_mapping_cmd = [
    'aws', 'apigateway', 'get-base-path-mapping', '--domain-name', cust_env['DOMAIN'], '--base-path', '(none)',
    '--query', 'restApiId'
]
base_path_mapping = None
try:
    base_path_mapping = json.loads(subprocess.check_output(base_path_mapping_cmd))
    if base_path_mapping == api_gateway_id:
        print 'Custom domain is correctly mapped to API Gateway'
    else:
        print 'Custom domain ({0}) is incorrectly mapped to API Gateway (saw {1}, expected {2})'.format(cust_env['DOMAIN'], base_path_mapping,  api_gateway_id)
        sys.exit(-1)
except:
    print 'Custom domain needs to be mapped to API Gatway'
    subprocess.call([
        'aws', 'apigateway', 'create-base-path-mapping',
        '--domain-name', cust_env['DOMAIN'],
        '--rest-api-id', api_gateway_id
    ])


if cust_env['CLEANUP'] == 'true':
    print '--> Cleanup all temp files'
    os.remove('config/dehydrated_config.txt')
    cert_files = glob.glob('certs/{0}/*'.format(cust_env['DOMAIN']))
    for f in cert_files:
        os.remove(f)
