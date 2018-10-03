FROM debian:stretch-slim
MAINTAINER Juan Luis Baptiste <juan.baptiste@gmail.com>
ENV VERSION 0.1.3

# COPY ping /ping
# COPY bandwidth /bandwidth
#COPY dist/network-tests-${VERSION}.tar.gz /opt
RUN apt-get update && \
    apt-get install --no-install-recommends -y apt-transport-https curl wget \
    gnupg2 iputils-ping python-pip python-setuptools sudo net-tools iproute2 && \
    pip install numpy pingparsing requests statistics && \
    rm -rf /var/lib/apt/lists/*
RUN curl -s https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo deb https://deb.nodesource.com/node_8.x bionic main > /etc/apt/sources.list.d/nodesource.list && \
    apt update && apt install --no-install-recommends -y nodejs && \
    npm install @sitespeed.io/throttle -g && \
    pip install --upgrade six && \
    rm -rf /var/lib/apt/lists/*
RUN  wget https://codeload.github.com/juanluisbaptiste/network-tests/tar.gz/v${VERSION} -O v${VERSION}.tar.gz
RUN tar zxvf /v${VERSION}.tar.gz -C /opt

WORKDIR /opt/network-tests-${VERSION}
RUN python setup.py install
#ENV PATH=$PATH:/ping:/bandwidth
CMD ["/bin/bash"]
