FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/
RUN rm -rvf apis/*_tests.py && rm -rvf apis/*_test.py && rm -rvf cypress && rm -rvf node_modules
RUN apk del nodejs npm
ENTRYPOINT [ "gunicorn","-b",":8080","-w","2","--threads","4","web_client:app" ]
