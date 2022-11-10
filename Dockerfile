FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

ADD requirements.txt /app/
WORKDIR /app

RUN set -e; \
  apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
  ;

RUN apk add --update python3-dev build-base
RUN  pip install --upgrade pip

RUN \
  pip install -r requirements.txt && \
  pip install mysql-connector-python \
  mysql.connector


RUN ln -sf /dev/stdout /var/log/nginx/access.log \
        && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./app /app