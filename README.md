## Api Gateway Custom Domain


Using [Lexicon](https://github.com/AnalogJ/lexicon) and [Dehydrated](https://github.com/lukas2511/dehydrated) This tool is to create ssl certs and domain details for api gateway

To use dehydrated with this certificate authority you have to agree to their terms of service which you can find here: https://letsencrypt.org/document
s/LE-SA-v1.1.1-August-1-2016.pdf


If you already have [Lexicon](https://github.com/AnalogJ/lexicon) and [Dehydrated](https://github.com/lukas2511/dehydrated) installed
you can run the following command:


	PROVIDER=CLOUDFLARE \
	LEXICON_CLOUDFLARE_USERNAME=? \
	LEXICON_CLOUDFLARE_TOKEN=? \
	AWS_ACCESS_KEY_ID=? \
	AWS_SECRET_ACCESS_KEY=? \
	DOMAIN=api.quietthyme.com \
	API_GATEWAY_NAME=dev-quietthyme-api \
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
