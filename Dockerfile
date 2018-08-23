FROM ubuntu:latest

MAINTAINER Tomas Holik "tomholik8@gmail.com"

USER root

RUN apt-get update -y
RUN apt-get install -y python-pip python3.6 python3.6-dev build-essential
RUN apt-get install -y wget
RUN apt-get install -y python3-distutils

RUN export DEBIAN_FRONTEND=noninteractive

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
RUN ln -s /usr/bin/python3.6 /usr/local/bin/python3

COPY . /pero
WORKDIR /pero

RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 2018
EXPOSE 443

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN python3.6 -m flask init-db
RUN python3.6 -m flask update-images images
RUN python3.6 -m flask set-group default

ENTRYPOINT ["python3.6", "-m"]
CMD ["flask", "run"]