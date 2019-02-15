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
RUN apt-get -y install apt-utils wget unzip vim openssh-client apache2 php iproute2 gnupg nano mlocate ntp
RUN wget -qO - http://download.rasdaman.org/packages/rasdaman.gpg | apt-key add - 
RUN echo "deb [arch=amd64] http://download.rasdaman.org/packages/deb bionic stable" | tee /etc/apt/sources.list.d/rasdaman.list
RUN apt-get -y update --fix-missing && \
      apt-get -y install rasdaman && \
      rm -rf /var/lib/apt/lists/* && \
      mkdir /opt/rasdaman/log  
#      mkdir /opt/rasdaman/log && \
#      /opt/rasdaman/bin/create_db.sh && \
#      /opt/rasdaman/bin/update_db.sh && \
#      /opt/rasdaman/bin/rasdaman_insertdemo.sh

RUN chmod 777 -R /opt/rasdaman/log

ENV RASMGR_PORT 7001
#ENV RASLOGIN rasadmin:d293a15562d3e70b6fdc5ee452eaed40
ENV RASLOGIN rasadmin:rasadmin

EXPOSE 7001-7010

# Update rasmgr.conf
#COPY rasmgr.conf.in /rasmgr.conf.in

# Naive check runs checks once a minute to see if either of the processes exited.
# If you wanna be elegant use supervisord
COPY entrypoint.sh /entrypoint.sh

#CMD ./entrypoint.sh


#RUN cp /opt/rasdaman/share/rasdaman/war/* /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/def.war /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/rasdaman.war /var/lib/tomcat8/webapps/
#COPY /opt/rasdaman/share/rasdaman/war/secoredb /var/lib/tomcat8/webapps/
#RUN chown -R tomcat8:tomcat8 /var/lib/tomcat8/webapps
RUN pip install glob2
RUN chmod 777 -R /opt/rasdaman/log


#start rasdaman
#WORKDIR /opt/rasdaman/bin
#CMD ["./start_rasdaman.sh"]
#RUN /opt/rasdaman/bin/start_rasdaman.sh

#Start apache2
EXPOSE 80
#RUN apache2ctl start

#SHELL ["/bin/bash", "-c"]
#start tomcat
EXPOSE 8080
#WORKDIR /etc/init.d
#CMD ["tomcat8", "start"]
#RUN /usr/share/tomcat8/bin/catalina.sh run
#RUN /usr/lib/jvm/default-java/bin/java \
#-Djava.util.logging.config.file=/var/lib/tomcat8/conf/logging.properties \
#-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager \
#-Djava.awt.headless=true \
#-XX:+UseConcMarkSweepGC \
#-Djdk.tls.ephemeralDHKeySize=2048 \
#-Djava.protocol.handler.pkgs=org.apache.catalina.webresources \
#-Dorg.apache.catalina.security.SecurityListener.UMASK=0027 \
#-Dignore.endorsed.dirs= \
#-classpath /usr/share/tomcat8/bin/bootstrap.jar:/usr/share/tomcat8/bin/tomcat-juli.jar \
#-Dcatalina.base=/var/lib/tomcat8 \
#-Dcatalina.home=/usr/share/tomcat8 \
#-Djava.io.tmpdir=/tmp/tomcat8-tomcat8-tmp \
#org.apache.catalina.startup.Bootstrap start &

# Start apache2
#EXPOSE 80
#WORKDIR /var/www/html
#CMD ["apache2ctl", "-D", "FOREGROUND"]
#RUN apache2ctl start

CMD /entrypoint.sh
