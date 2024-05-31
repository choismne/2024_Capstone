FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3-pip vim pkg-config libmysqlclient-dev

RUN pip3 install fastapi uvicorn pkgconfig mysqlclient \
    sqlalchemy passlib python-jose python-jose[cryptography] python-multipart boto3 gunicorn

ENV AUTH_SECRET_KEY <SECRET KEY>

WORKDIR /app

ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
