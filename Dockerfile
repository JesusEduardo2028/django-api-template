FROM python:3.7-alpine
MAINTAINER Jmunoz

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./entrypoint.sh /entrypoint.sh

# apk is the Package manager that comes with alpine
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
RUN adduser -D user
RUN chown user /entrypoint.sh && chmod +x /entrypoint.sh

USER user

EXPOSE 8000
CMD ["sh","-c","python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
