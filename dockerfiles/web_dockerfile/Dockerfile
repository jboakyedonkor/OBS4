FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/
RUN rm -rvf apis/*_tests.py && rm -rvf apis/*_test.py && rm -rvf cypress
RUN apk del nodejs npm
#ENTRYPOINT [ "gunicorn","-b",":8080","-w","1","--threads","1","web_client:app" ]
ENTRYPOINT [ "gunicorn","-b",":8080","web_client:app" ]
