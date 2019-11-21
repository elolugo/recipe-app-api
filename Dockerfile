FROM python:3.7-alpine
MAINTAINER Alejandro Lugo

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt

# Install the postgresql client for postgres and psycopg2
RUN apk add --update --no-cache postgresql-client jpeg-dev

# Installing some dependencies for psycopg2 and Pillow
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt

# Removing the dependencies for installing psycopg2
RUN apk del .tmp-build-deps

# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

# Creating the directories for serving the images and other files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Creating a user different than root
RUN adduser -D user

# Giving the owner rights of the static directories to user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/

USER user
