#FROM python:2.7.13
FROM ubuntu:latest
MAINTAINER Juan Luis Baptiste <juan.baptiste@gmail.com>
ENV VERSION 0.1.2

# COPY ping /ping
# COPY bandwidth /bandwidth
#COPY dist/network-tests-${VERSION}.tar.gz /opt
RUN apt-get update && \
    apt-get install -y curl wget iputils-ping python-pip && \
    pip install numpy pingparsing requests statistics
RUN curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo deb https://deb.nodesource.com/node_8.x bionic main > /etc/apt/sources.list.d/nodesource.list && \
    apt update && apt install -y nodejs && \
    npm install @sitespeed.io/throttle -g
RUN  wget https://codeload.github.com/juanluisbaptiste/network-tests/tar.gz/v${VERSION} -O v${VERSION}.tar.gz
RUN tar zxvf /v${VERSION}.tar.gz -C /opt

WORKDIR /opt/network-tests-${VERSION}
RUN python setup.py install
#ENV PATH=$PATH:/ping:/bandwidth
CMD ["/bin/bash"]
