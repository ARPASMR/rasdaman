# Start from scratch
FROM docker.io/tomcat:7.0.91-jre7

# Label this image
# LABEL name="registry.arpa.local/servizi/rasdaman"
LABEL name="local:rasdaman"
LABEL version="1.0"
LABEL maintainer="Luca Paganotti <luca.paganotti@gmail.com>"
LABEL description="image for rasdaman container"

# Update system
RUN apt-get -y update --fix-missing && \
      apt-get -y upgrade --fix-missing && \
      apt-get -y autoremove && \
      apt-get -y install apt-utils wget unzip && \
      apt-get -y install vim && \
      wget -O - http://download.rasdaman.org/packages/rasdaman.gpg | apt-key add - && \
      echo "deb [arch=amd64] http://download.rasdaman.org/packages/deb trusty stable" | tee /etc/apt/sources.list.d/rasdaman.list && \
      apt-get -y update --fix-missing && \
      apt-get -y install rasdaman && \
      rm -rf /var/lib/apt/lists/* && \
      mkdir /opt/rasdaman/log && \
      /opt/rasdaman/bin/create_db.sh && \
      /opt/rasdaman/bin/update_db.sh && \
      /opt/rasdaman/bin/rasdaman_insertdemo.sh

ENV RASMGR_PORT 7001
ENV RASLOGIN rasadmin:d293a15562d3e70b6fdc5ee452eaed40

EXPOSE 7001-7010

# Update rasmgr.conf
COPY rasmgr.conf.in /rasmgr.conf.in

# Naive check runs checks once a minute to see if either of the processes exited.
# If you wanna be elegant use supervisord
COPY entrypoint.sh /entrypoint.sh

CMD ./entrypoint.sh

