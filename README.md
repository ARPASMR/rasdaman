## rasdaman

This repository contains the initial _Dockerfile_ for a rasdman only container and the _entrypoint.sh_ bash script that starts rasdaman as a service in the docker container and keeps the container alive.

## Persistent data

Persistent data are included in the "data" folder. 

NB: The fwi_grid_demo data is only an extract of the complete dataset of data which need to be imported in Rasdaman by ARPA Lombardia
In the fwi_grid_demo data there are two python scripts used to import data in rasdaman.

## Command examples
`
docker run -d -it --rm --name rasdaman local:rasdaman
`

Starts the container with no persistence on docker's volumes

```
docker run -d -it --rm --name rasdaman --mount type=bind,src=/host/local/path,dst=/opt/rasdaman/data local:rasdaman
```


Starts the container with a bind volume and RASMGR_HOST_IP environment variable

```
[...]
```

# prerequisites
__petascopedb__
```
docker run -d --name rasdatabase -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=<user> -e POSTGRES_DB=<petascopedb> -v /home/meteo/database/data/rasdaman:/var/lib/postgresql/data -p 5428:5432 postgres:9.3
```
(see followng 3 point)


1. Starts the container with persistence volumes:

- -v /home/meteo/data/sqlite:/opt/rasdaman/data  --> rasdaman DB
- -v /home/meteo/data/fwi_grid:/opt/rasdaman/fwi_grid --> Milanone folder **previosly mounted on Sinergico03**
- -v /home/meteo/data/etc_rasdaman:/opt/rasdaman/etc --> Rasdaman and Petascope configuration files
- -v /home/meteo/data/tomcat8_webapps:/var/lib/tomcat8/webapps --> Rasdaman.war (java  .war files)
- -v /home/meteo/data/demo_client:/var/www/html/demo_client --> apache client (demo GTER to access to WMS webservices)
- -v /home/meteo/data/scripts:/opt/rasdaman/scripts --> python script to import data

2. with the following port open: 

- 8080 for tomcat8
- 808 for apache2
- 7001 for rasdaman 

3. with a link to a PostgreSQL DB (for petascope) in anoher container rasdatabase:rasdatabase

4.and with the proxy http and https configured:

- -e “http_proxy=http://<user>:<password>@proxy2.arpa.local:8080” 
- -e “https_proxy=https://<user>:<password>@proxy2.arpa.local:8080”

```
docker run --name myras --link rasdatabase:rasdatabase -d \
        -v /home/meteo/data/sqlite:/opt/rasdaman/data \
        -v /home/meteo/data/fwi_grid:/opt/rasdaman/fwi_grid \
        -v /home/meteo/data/etc_rasdaman:/opt/rasdaman/etc \
        -v /home/meteo/data/tomcat8_webapps:/var/lib/tomcat8/webapps \
        -v /home/meteo/data/demo_client:/var/www/html/demo_client \
        -v /home/meteo/data/scripts:/etc/scripts \
        -e “http_proxy=http://<user>:<password>@proxy2.arpa.local:8080” \
        -e “https_proxy=https://<user>:<password>@proxy2.arpa.local:8080” \
        -p 8080:8080 -p 808:80 -p 7001:70001\
        arpasmr/rasdaman:bionic
```

## Ports

Ports exposed: 
- from 7001 to 7010 (only 7001 mandatory)
- 80 (apache)
- 8080 (tomcat)



## Open problems


service tomcat8 start (che stranamente da un messaggio "fail" ma in realtà parte correttamente)


## Docker instruction
To view the docker containers running:
```
docker ps -a   
```
To connect to the myras container:
```
docker exec -it rasdaman /bin/bash
```
To stop the container:
```
docker stop rasdaman

#only if container is launched without -rm command
docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm

```


# Example
```
docker run -d --rm -e RASMGR_HOST_IP="172.17.0.2" --name rasdaman -v /home/meteo/Projects/rasdaman/sqlite:/opt/rasdaman/data -v /home/meteo/Projects/rasdaman/etc_rasdaman:/opt/rasdaman/etc -v /home/meteo/Projects/rasdaman/tomcat8_webapps:/var/lib/tomcat8/webapps -v /home/meteo/Projects/rasdaman/demo_client:/var/www/html/demo_client -v /home/meteo/Projects/rasdaman/crontab:/etc/crontab -p 8080:8080 -p 808:80 -v /home/meteo/data/fwi_grid:/opt/rasdaman/fwi_grid --link rasdatabase -e "http_proxy=<proxy>" -e "https_proxy=<proxy>" rasdaman
 ```
