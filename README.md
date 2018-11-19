## rasdaman

This repository contains the initial _Dockerfile_ for a rasdman only container and the _entrypoint.sh_ bash script that starts rasdaman as a service in the docker container and keeps the container alive.

## Command examples
`
docker run -d -it --rm --name rasdaman local:rasdaman
`

Starts the container with no persistence on docker's volumes

```
docker run -d -it --rm -e RASMGR_HOST_IP="172.17.0.2" --name rasdaman --mount type=bind,src=/host/local/path,dst=/opt/rasdaman/data local:rasdaman
```


Starts the container with a bind volume and RASMGR_HOST_IP environment variable

```
[...]
```


Starts the container with persistence volumes:

- v /home/meteo/data/sqlite:/opt/rasdaman/data  --> rasdaman DB
- v /home/meteo/data/fwi_grid:/opt/rasdaman/fwi_grid --> Milanone folder previosly mounted on Sinergico03
- v /home/meteo/data/etc_rasdaman:/opt/rasdaman/etc --> Rasdaman and Petascope configuration files
- v /home/meteo/data/tomcat8_webapps:/var/lib/tomcat8/webapps --> Rasdaman.war (java  .war files)
- v /home/meteo/data/demo_client:/var/www/html/demo_client --> apache client (demo GTER to access to WMS webservices)
- v /home/meteo/data/crontab:/etc/crontab --> crontab which import data every morning (7:00 UTC)

and with the following port open: 

- 8080 for tomcat8
- 808 for apache2

```
docker run --name myras --link rasdatabase:rasdatabase -d -v /home/meteo/data/sqlite:/opt/rasdaman/data -v /home/meteo/data/fwi_grid:/opt/rasdaman/fwi_grid -v /home/meteo/data/etc_rasdaman:/opt/rasdaman/etc -v /home/meteo/data/tomcat8_webapps:/var/lib/tomcat8/webapps -v /home/meteo/data/demo_client:/var/www/html/demo_client -v /home/meteo/data/crontab:/etc/crontab  -p 8080:8080 -p 808:80 arpasmr/rasdaman:bionic
```

## Ports

Ports exposed: from 7001 to 7010 (only 7001 mandatory)

## Environment variables

**RASMGR_HOST_IP** substitutes host value in rasmgr.conf with this variable value.

