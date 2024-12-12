FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000
