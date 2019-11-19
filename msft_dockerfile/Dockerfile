FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/apis/
RUN echo $PORT
ENTRYPOINT [ "gunicorn","-b",":8080","-w","4","--threads","8","msft_api:microsoft_api" ]
