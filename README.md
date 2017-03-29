## Api Gateway Custom Domain


Using [Lexicon](https://github.com/AnalogJ/lexicon) and [Dehydrated](https://github.com/lukas2511/dehydrated), automatically register custom domains in API Gateway with Letsencrypt SSL certificates. See http://blog.thesparktree.com/post/152904762374/custom-domains-for-aws-lambdaapi-gateway-using

If you already have [Lexicon](https://github.com/AnalogJ/lexicon) and [Dehydrated](https://github.com/lukas2511/dehydrated) installed
you can run the following command:


	PROVIDER=cloudflare \
	LEXICON_CLOUDFLARE_USERNAME=? \
	LEXICON_CLOUDFLARE_TOKEN=? \
	AWS_ACCESS_KEY_ID=? \
	AWS_SECRET_ACCESS_KEY=? \
	DOMAIN=api.quietthyme.com \
	API_GATEWAY_NAME=dev-quietthyme-api \
	DOMAIN_BASE_PATH_MAPPING=? \
	python api-gateway-custom-domain.py


or, if you only have docker installed:

	docker run \
	-e PROVIDER=CLOUDFLARE \
	-e LEXICON_CLOUDFLARE_USERNAME \
	-e LEXICON_CLOUDFLARE_TOKEN \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_DEFAULT_REGION \
	-e AWS_SECRET_ACCESS_KEY \
	-e DOMAIN=api.quietthyme.com \
	-e API_GATEWAY_NAME=dev-quietthyme-api \
	-v $(pwd)/certs:/srv/certs \
	analogj/aws-api-gateway-letsencrypt
