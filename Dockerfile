FROM python:3.7-alpine

EXPOSE 5000
WORKDIR /OBS4
COPY . .
RUN apk --no-cache add build-base
RUN pip install -r requirements.txt

CMD ["python3","apis/fb_tests.py"]
