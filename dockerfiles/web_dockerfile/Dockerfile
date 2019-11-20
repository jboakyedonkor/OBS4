FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/
RUN rm -rvf apis
ENTRYPOINT [ "gunicorn","-b",":8080","-w","2","--threads","4","web_client:app" ]
