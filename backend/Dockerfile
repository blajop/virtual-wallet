# syntax=docker/dockerfile:1

FROM python:alpine3.18

WORKDIR /root

COPY requirements.txt requirements.txt

RUN apk add build-base
RUN apk add mariadb-dev
RUN pip install -r requirements.txt

COPY . /root

EXPOSE 5555

ENTRYPOINT ["python3", "-m" , "main"]

