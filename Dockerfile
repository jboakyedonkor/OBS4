FROM python:3.7-alpine

ARG MSFT_FIREBASE_API_KEY_G


ENV MSFT_FIREBASE_API_KEY MSFT_FIREBASE_API_KEY_G
ENV
ENV


EXPOSE 5000
EXPOSE 5432

WORKDIR /OBS4
COPY . .
RUN apk --no-cache add build-base
RUN pip install -r requirements.txt

CMD ["python3","apis/fb_tests.py"]
