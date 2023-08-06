FROM alpine
FROM python:3.7-slim

RUN apt-get update && apt-get install -y \
    git

ADD . /app
WORKDIR /app

RUN pip install pip --upgrade
RUN pip install -r requirements.txt
RUN pip install pytest pytest-cov pylint
