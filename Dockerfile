FROM ubuntu:16.04

MAINTAINER Princip <principle.main@gmail.com>

ENV WORKING_DIR /distr

WORKDIR $WORKING_DIR

ADD ./distr $WORKING_DIR

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN chmod 755 $WORKING_DIR
RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential python3 python3-dev python3-pip curl apt-transport-https software-properties-common ca-certificates -y
RUN pip3 install --upgrade pip
RUN curl -fsSL https://yum.dockerproject.org/gpg | apt-key add -
RUN add-apt-repository "deb https://apt.dockerproject.org/repo/ ubuntu-$(lsb_release -cs) main"
RUN apt-get update
RUN apt-get -y install docker-engine=1.13.0-0~ubuntu-xenial
RUN cd $WORKING_DIR
RUN chmod 755 run.sh
RUN pip3 install virtualenv
RUN virtualenv .
RUN source ./bin/activate
RUN pip3 install -r requirements.txt

# Windows add specific CR LF to the end of line
RUN sed -i -e 's/\r$//' run.sh

EXPOSE 5000

CMD ./run.sh
