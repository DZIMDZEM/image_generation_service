FROM python:3.10-slim-bullseye

EXPOSE 8080

COPY requirements-api.txt /app/requirements-api.txt

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install gunicorn
RUN which gunicorn


RUN pip install -r requirements-api.txt


COPY . /app

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8080", "--preload", "--threads=20", "local_server:create_app()"]
