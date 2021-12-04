FROM python:3.9-buster

RUN apt update 
RUN useradd python -u 1000 -m

WORKDIR /home/python/app
RUN pip install black fastapi uvicorn[standard] python-multipart pytest requests pytest-watch