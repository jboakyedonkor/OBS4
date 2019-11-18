FROM python:3.7-alpine

ARG MSFT_FIREBASE_API_KEY_G
ARG MSFT_FIREBASE_AUTH_DOMAIN_G
ARG MSFT_FIREBASE_DB_URL_G
ARG MSFT_FIREBASE_PROJECT_ID_G
ARG MSFT_FIREBASE_STORAGE_BUCKET_G
ARG MSFT_FIREBASE_MSG_SENDER_ID_G
ARG MSFT_FIREBASE_APP_ID_G
ARG SECRET_KEY_G
ARG MSFT_TRADIER_API_KEY_G

ARG AAPL_FIRE_API_KEY_G
ARG AAPL_AUTH_DOMAIN_G
ARG AAPL_DATABASE_URL_G
ARG AAPL_PROJECT_ID_G
ARG AAPL_STORAGE_BUCKET_G
ARG AAPL_MESS_SENDER_ID_G
ARG AAPL_APP_ID_G
ARG AAPL_BEARER_G
ARG SQLALCHEMY_DATABASE_URI_G

ARG FB_ACCESS_TOKEN_G
ARG FB_FIREBASE_API_KEY_G 
ARG FB_FIREBASE_APP_ID_G
ARG FB_FIREBASE_AUTH_DOMAIN_G
ARG FB_FIREBASE_DB_URL_G
ARG FB_FIREBASE_MEASUREMENT_ID_G
ARG FB_FIREBASE_MSG_SENDER_ID_G
ARG FB_FIREBASE_PROJECT_G 
ARG FB_FIREBASE_STORAGE_BUCKET_G 

ENV MSFT_FIREBASE_API_KEY MSFT_FIREBASE_API_KEY_G
ENV MSFT_FIREBASE_AUTH_DOMAIN MSFT_FIREBASE_AUTH_DOMAIN_G
ENV MSFT_FIREBASE_DB_URL MSFT_FIREBASE_DB_URL_G
ENV MSFT_FIREBASE_PROJECT_ID MSFT_FIREBASE_PROJECT_ID_G
ENV MSFT_FIREBASE_STORAGE_BUCKET MSFT_FIREBASE_STORAGE_BUCKET_G
ENV MSFT_FIREBASE_MSG_SENDER_ID MSFT_FIREBASE_MSG_SENDER_ID_G
ENV MSFT_FIREBASE_APP_ID MSFT_FIREBASE_APP_ID_G
ENV SECRET_KEY SECRET_KEY_G
ENV MSFT_TRADIER_API_KEY MSFT_TRADIER_API_KEY_G

ENV AAPL_FIRE_API_KEY AAPL_FIRE_API_KEY_G
ENV AAPL_AUTH_DOMAIN AAPL_AUTH_DOMAIN_G
ENV AAPL_DATABASE_URL AAPL_DATABASE_URL_G
ENV AAPL_PROJECT_ID AAPL_PROJECT_ID_G
ENV AAPL_STORAGE_BUCKET AAPL_STORAGE_BUCKET_G
ENV AAPL_MESS_SENDER_ID AAPL_MESS_SENDER_ID_G
ENV AAPL_APP_ID AAPL_APP_ID_G
ENV AAPL_BEARER AAPL_BEARER_G
ENV SQLALCHEMY_DATABASE_URI SQLALCHEMY_DATABASE_URI_G

ENV FB_ACCESS_TOKEN FB_ACCESS_TOKEN_G
ENV FB_FIREBASE_API_KEY FB_FIREBASE_API_KEY_G 
ENV FB_FIREBASE_APP_ID FB_FIREBASE_APP_ID_G 
ENV FB_FIREBASE_AUTH_DOMAIN FB_FIREBASE_AUTH_DOMAIN_G 
ENV FB_FIREBASE_DB_URL FB_FIREBASE_DB_URL_G 
ENV FB_FIREBASE_MEASUREMENT_ID FB_FIREBASE_MEASUREMENT_ID_G 
ENV FB_FIREBASE_MSG_SENDER_ID FB_FIREBASE_MSG_SENDER_ID_G 
ENV FB_FIREBASE_PROJECT FB_FIREBASE_PROJECT_G 
ENV FB_FIREBASE_STORAGE_BUCKET FB_FIREBASE_STORAGE_BUCKET_G 




ENV PORT 8080

EXPOSE 5000
EXPOSE 5001
EXPOSE 5432

WORKDIR /OBS4
COPY . .
RUN rm  -v *.png
RUN rm  -v *.yaml
RUN rm  -v *.json
RUN rm  -rvf venv
RUN rm  -rvf *_dockerfile/
RUN rm  -v README.md
RUN apk --no-cache add build base
RUN apk update && apk --no-cache add postgresql-dev
RUN pip3 install  -r requirements.txt
