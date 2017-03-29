FROM python:2-alpine
MAINTAINER Jason Kulatunga <jason@thesparktree.com>
LABEL name="aws-api-gateway-letsencrypt"
LABEL version="1.0"

RUN apk add --update --no-cache \
	bash \
	curl \
	openssl \
	git \
	&& rm -rf /var/cache/apk/*

# Install dehydrated (letsencrypt client), awscli & dns-lexicon
RUN git clone --depth 1 https://github.com/lukas2511/dehydrated.git /srv/dehydrated && \
	pip install --upgrade pip && \
	pip install --upgrade awscli  && \
	pip install dns-lexicon

ENV PATH=/srv/dehydrated:$PATH \
    AWS_DEFAULT_REGION=ap-southeast-1

# Copy over dehydrated hook file & startup script
COPY . /srv/

WORKDIR /srv
ENTRYPOINT ["python", "api-gateway-custom-domain.py"]