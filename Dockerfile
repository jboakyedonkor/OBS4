FROM python:3.7-alpine

EXPOSE 5000
WORKDIR /OBS4
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3","./apis/msft_tests.py" ]