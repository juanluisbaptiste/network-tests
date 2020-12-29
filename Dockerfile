FROM debian:buster-slim
MAINTAINER Juan Luis Baptiste <juan.baptiste@gmail.com>
ENV VERSION 0.1.5

RUN apt-get update && \
    apt-get install --no-install-recommends -y apt-transport-https cron curl wget \
    gnupg2 iputils-ping python3-pip python3-setuptools python3-wheel rsyslog sendemail sudo telnet net-tools iproute2 zip npm && \
    pip3 install numpy pingparsing requests statistics supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    npm install @sitespeed.io/throttle -g && \
    pip3 install --upgrade six && \
    rm -rf /var/lib/apt/lists/*
RUN  wget https://codeload.github.com/juanluisbaptiste/network-tests/tar.gz/v${VERSION} -O v${VERSION}.tar.gz && \
     tar zxvf /v${VERSION}.tar.gz -C /opt && \
     rm -f /v${VERSION}.tar.gz
COPY tests/* /
COPY *.sh /
COPY files/docker/etc/supervisord.d/*.ini /etc/supervisord.d/
COPY files/templates/* /templates/

WORKDIR /opt/network-tests-${VERSION}
RUN python3 setup.py install && \
    chmod 755 /*.sh && \
    mkdir /var/log/supervisor
WORKDIR /
#ENV PATH=$PATH:/ping:/bandwidth
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["bash"]
