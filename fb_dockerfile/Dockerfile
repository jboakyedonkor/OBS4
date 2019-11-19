FROM gcr.io/obs4-259117/obs4:latest
WORKDIR /OBS4/apis/
RUN rm -rvf *_tests.py && rm -rvf *_test.py
ENTRYPOINT [ "gunicorn","-b",":$PORT","-w","4","--threads","8","fb_api:app" ]