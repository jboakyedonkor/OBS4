FROM python:3.7-alpine

EXPOSE 5000
WORKDIR /OBS4
COPY . .
COPY apis/fb_tests.py .
RUN apk --no-cache add build-base
RUN pip install -r requirements.txt

CMD ["fb_tests.py"]