FROM gcr.io/google-appengine/python:latest

EXPOSE 5000
WORKDIR /OBS4
COPY . .
RUN pip -r requirments.txt

ENTRYPOINT [ "python3","./apis/msft_tests.py" ]