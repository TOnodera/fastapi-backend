FROM python:3.9-buster

RUN apt update 
# 開発用tmux vim
RUN apt install -y tmux vim
RUN useradd python -u 1000 -m

WORKDIR /home/python/app
RUN pip install black fastapi uvicorn[standard] python-multipart pytest requests pytest-watch pytest-testmon \
        && pip install sqlalchemy psycopg2 pytest-env