#FROM python:2.7.13
FROM ubuntu:latest
MAINTAINER Juan Luis Baptiste <juan.baptiste@gmail.com>

COPY ping /ping
COPY bandwidth /bandwidth

RUN apt-get update && \
    apt-get install -y iputils-ping python-pip && \
    pip install --upgrade pip && \
    pip install datetime pingparsing requests statistics && \
    chmod 755 /ping/ping-test.py /bandwidth/*-speed.py
ENV PATH=$PATH:/ping:/bandwidth
CMD ["/bin/bash"]
