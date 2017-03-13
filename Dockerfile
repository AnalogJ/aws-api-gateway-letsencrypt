FROM python:2-alpine

MAINTAINER Itoc <devops@itoc.com.au>

LABEL name="aws-api-gateway-letsencrypt"
LABEL version="1.0"

RUN apk add --update --no-cache \
	bash \
	curl \
	openssl \
	git \
	groff \
	less

# Install dehydrated (letsencrypt client), awscli & dns-lexicon
RUN git clone --depth 1 https://github.com/itoc/dehydrated.git /srv/dehydrated && \
	pip install --upgrade pip && \
	pip install awscli --upgrade && \
	pip install git+https://github.com/itoc/lexicon.git@v1.2.5#egg=dns-lexicon[route53]

ENV PATH=/srv/dehydrated:$PATH \
    AWS_DEFAULT_REGION=ap-southeast-1 \
    PROVIDER=route53
# Copy over dehydrated hook file & startup script
COPY . /srv/

WORKDIR /srv
ENTRYPOINT ["python", "api-gateway-custom-domain.py"]