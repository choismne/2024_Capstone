FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3-pip vim

RUN pip3 install fastapi uvicorn db-sqlite3 \
    sqlalchemy passlib python-jose python-jose[cryptography] python-multipart

#docker build -t 이미지명 : 태그
#docker run -it  --name captone-fastapi -p 8080:8000 -v /Users/choismn/Desktop/2024_Capstone/backend-fastapi:/app fastapi:latest