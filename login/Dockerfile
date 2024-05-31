FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3-pip vim pkg-config libmysqlclient-dev

RUN pip3 install fastapi uvicorn pkgconfig mysqlclient \
    sqlalchemy passlib python-jose python-jose[cryptography] python-multipart boto3 gunicorn

ENV AUTH_SECRET_KEY 1f45c681bf9fb2d329d544efeabf346db688be94974338d1e987cdc2ecba9d9f

WORKDIR /app

ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]

#docker build -t 이미지명 : 태그
#docker run -it  --name captone-fastapi -p 8080:8000 -v /Users/choismn/Desktop/2024_Capstone/backend-fastapi:/app fastapi:latest