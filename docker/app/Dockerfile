FROM python:3.7-alpine
MAINTAINER Jmunoz

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# apk is the Package manager that comes with alpine
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./docker/app/entrypoint /entrypoint

RUN adduser -D user
RUN chown user /entrypoint/*.sh && chmod +x /entrypoint/*.sh

USER user

EXPOSE 8000
