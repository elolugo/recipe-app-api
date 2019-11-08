FROM python:3.7-alpine
MAINTAINER Alejandro Lugo

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
# Install the postgresql client for postgres and psycopg2
RUN apk add --update --no-cache postgresql-client
# Installing some dependencies for psycopg2
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# Removing the dependencies for installing psycopg2
RUN apk del .tmp-build-deps

# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

RUN adduser -D user
USER user
