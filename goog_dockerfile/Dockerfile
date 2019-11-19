FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/apis/
RUN echo $PORT
ENTRYPOINT [ "gunicorn","-b",":$PORT","-w","4","--threads","8","gogg_api:app" ]