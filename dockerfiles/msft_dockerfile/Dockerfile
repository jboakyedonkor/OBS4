FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/apis/
RUN rm -rvf *_tests.py && rm -rvf *_test.py && rm -rvf cypress && rm -rvf node_modules
RUN apk del nodejs npm
ENTRYPOINT [ "gunicorn","-b",":8080","-w","2","--threads","4","msft_api:microsoft_api" ]
