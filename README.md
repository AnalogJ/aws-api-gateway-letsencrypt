## Api Gateway Custom Domain

Forked version for review purposes.

Using [Lexicon](https://github.com/itoc/lexicon) and [Dehydrated](https://github.com/itoc/dehydrated) This tool is to create ssl certs and domain details for api gateway

To use dehydrated with this certificate authority you have to agree to their terms of service which you can find here: https://letsencrypt.org/document
s/LE-SA-v1.1.1-August-1-2016.pdf

	docker run \
		-v $(pwd)/accounts:/dehydrated/accounts \
		--entrypoint "" \
		itoc/aws-api-gateway-letsencrypt \
		dehydrated --register --accept-terms

	docker run \
	-e PROVIDER=ROUTE53 \
	-e LEXICON_ROUTE53_USERNAME \
	-e LEXICON_ROUTE53_TOKEN \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_DEFAULT_REGION \
	-e AWS_SECRET_ACCESS_KEY \
	-e DOMAIN=api.quietthyme.com \
	-e API_GATEWAY_NAME=dev-quietthyme-api \
	-v $(pwd)/certs:/srv/certs \
	itoc/aws-api-gateway-letsencrypt
