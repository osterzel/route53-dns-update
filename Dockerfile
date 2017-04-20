FROM ubuntu:16.04

RUN apt-get update && apt-get install -fy python-pip && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY r53.py /app

ENTRYPOINT [ "./r53.py" ]
