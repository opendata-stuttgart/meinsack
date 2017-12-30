FROM python:3.6
MAINTAINER Stuttgart Python Interest Group

EXPOSE 8010

ENV DEBIAN_FRONTEND noninteractive

USER root
RUN apt-get update && apt-get install -y ttf-dejavu-core

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
ADD . /opt/code

# user
RUN useradd uid1000 -d /home/uid1000
RUN mkdir -p /home/uid1000 && chown uid1000: /home/uid1000
VOLUME /home/uid1000
RUN chown -R uid1000: /opt

WORKDIR /opt/code/sack

# uid1000 is created in aexea-base
USER uid1000

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
