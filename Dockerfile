FROM aexea/aexea-base:py3.6
MAINTAINER Stuttgart Python Interest Group

EXPOSE 8010

USER root
RUN apt-get update && apt-get install -y ttf-dejavu-core

ADD requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip install --find-links=http://pypi.qax.io/wheels/ --trusted-host pypi.qax.io -Ur requirements.txt
ADD . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/sack

# uid1000 is created in aexea-base
USER uid1000

# production stuff
ENTRYPOINT ["./start.sh"]
CMD ["web"]
