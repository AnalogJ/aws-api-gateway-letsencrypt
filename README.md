

	docker run \
	-e LEXICON_CLOUDFLARE_USERNAME \
	-e LEXICON_CLOUDFLARE_TOKEN \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY \
	-e DOMAIN=api.quietthyme.com \
	-e API_GATEWAY_NAME=dev-quietthyme-api \
	-v `pwd`/certs:/srv/certs \
	analogj/aws-api-gateway-letsencrypt