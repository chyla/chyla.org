FROM docker.io/library/ubuntu:24.10

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 python3-venv python3-pip
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
RUN pip install setuptools

CMD /bin/bash
