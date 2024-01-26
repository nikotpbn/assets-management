FROM python:3.12.1-alpine
LABEL maintainer="nikotpbn"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc musl-dev linux-headers python3-dev && \
    apk add --update --no-cache mariadb-dev jpeg-dev && \
    pip install -r requirements.txt && \
    apk del .tmp-build-deps

EXPOSE 8000