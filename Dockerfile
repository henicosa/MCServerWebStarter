# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y iputils-ping
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

ENV FLASK_APP app.py

ENTRYPOINT ["python", "-m", "gunicorn", "-b 0.0.0.0:8000", "app:app"]
