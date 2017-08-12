FROM        amazonlinux
MAINTAINER  tomislacker

ENV PYTHON_VERSION=3.6.2

WORKDIR /tmp
RUN     yum -y groupinstall development \
        && yum -y install \
            openssl-devel \
            xz \
            zlib-devel \
        && curl \
            -o Python-${PYTHON_VERSION}.tar.xz \
            https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
        && tar xJf Python-${PYTHON_VERSION}.tar.xz \
        && cd /tmp/Python-${PYTHON_VERSION} \
        && ./configure \
        && make \
        && make install \
        && cd .. \
        && rm -fr Python* \
        && pip3 install --upgrade virtualenv

COPY        builder.sh /builder.sh
RUN         chmod 755 /builder.sh
ENTRYPOINT  /builder.sh
