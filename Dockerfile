FROM docker pull gcr.io/google-appengine/python:latest

EXPOSE 5000

ADD apis /usr/src/app/apis
ADD web_client /usr/src/app/web_client
