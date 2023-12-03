# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /person-playlist-generator
COPY . /person-playlist-generator

RUN pip3 install -r requirements.txt

CMD [ "flask", "--debug", "run", "-h", "localhost", "-p", "8080" ]
