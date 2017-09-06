#FROM python:2.7.13
FROM ubuntu:latest
MAINTAINER Juan Luis Baptiste <juan.baptiste@gmail.com>
ENV VERSION 0.1.1

# COPY ping /ping
# COPY bandwidth /bandwidth
COPY dist/network-tests-${VERSION}.tar.gz /opt
RUN apt-get update && \
    apt-get install -y iputils-ping python-pip && \
    pip install --upgrade pip && \
    pip install numpy pingparsing requests statistics && \
    tart -C /opt zxvf /opt/network-tests-${VERSION}.tar.gz 
WORKDIR /opt
#ENV PATH=$PATH:/ping:/bandwidth
CMD ["/bin/bash"]
