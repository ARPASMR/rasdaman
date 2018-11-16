# Start from scratch
FROM ubuntu:bionic

# Label this image
# LABEL name="registry.arpa.local/servizi/rasdaman"
LABEL name="local:rasdaman"
LABEL version="1.0"
LABEL maintainer="Luca Paganotti <luca.paganotti@gmail.com>"
LABEL description="image for rasdaman container with Ubuntu 18.04"

# To run dpkg (behind other tools like Apt) without interactive dialogue, you can set one environment variable as
ENV DEBIAN_FRONTEND noninteractive

# Update system
RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade --fix-missing 
RUN apt-get -y autoremove
RUN apt-get -y install apt-utils wget unzip
RUN apt-get -y install vim
RUN apt-get -y install openssh-client 
RUN apt-get -y install apache2
RUN apt-get -y install iproute2
RUN apt-get -y install gnupg
RUN apt-get -y install nano mlocate
RUN wget -qO - http://download.rasdaman.org/packages/rasdaman.gpg | apt-key add - 
RUN echo "deb [arch=amd64] http://download.rasdaman.org/packages/deb bionic stable" | tee /etc/apt/sources.list.d/rasdaman.list
RUN apt-get -y update --fix-missing && \
      apt-get -y install rasdaman && \
      rm -rf /var/lib/apt/lists/* && \
      mkdir /opt/rasdaman/log && \
      /opt/rasdaman/bin/create_db.sh && \
      /opt/rasdaman/bin/update_db.sh && \
      /opt/rasdaman/bin/rasdaman_insertdemo.sh

RUN chmod 777 -R /opt/rasdaman/log

ENV RASMGR_PORT 7001
ENV RASLOGIN rasadmin:d293a15562d3e70b6fdc5ee452eaed40

EXPOSE 7001-7010

# Update rasmgr.conf
COPY rasmgr.conf.in /rasmgr.conf.in

# Naive check runs checks once a minute to see if either of the processes exited.
# If you wanna be elegant use supervisord
COPY entrypoint.sh /entrypoint.sh

CMD ./entrypoint.sh


#RUN cp /opt/rasdaman/share/rasdaman/war/* /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/def.war /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/rasdaman.war /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/secoredb /var/lib/tomcat8/webapps/
#RUN chown -R tomcat8:tomcat8 /var/lib/tomcat8/webapps
RUN pip install glob2
RUN chmod 777 -R /opt/rasdaman/log


#start rasdaman
WORKDIR /opt/rasdaman/bin
CMD ["start_rasdaman.sh"]


#start tomcat
EXPOSE 8080
WORKDIR /etc/init.d
CMD ["tomcat8", "start"]


# Start apache2
EXPOSE 80
WORKDIR /var/www/html
CMD ["apache2ctl", "-D", "FOREGROUND"]
