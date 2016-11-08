FROM python:2-alpine
MAINTAINER Jason Kulatunga <jason@thesparktree.com>

RUN apk add --update \
	bash \
	curl \
	openssl \
	git \
	&& rm -rf /var/cache/apk/*

# Install dehydrated (letsencrypt client), awscli & dns-lexicon
RUN git clone --depth 1 https://github.com/lukas2511/dehydrated.git /srv/dehydrated && \
	pip install --upgrade pip && \
	pip install dns-lexicon awscli

ENV PATH /srv/dehydrated:$PATH

# Copy over dehydrated hook file & startup script
COPY . /srv/
RUN chmod +x /srv/config/dehydrated.hook.sh

WORKDIR /srv
ENTRYPOINT ["python", "api-gateway-custom-domain.py"]