## rasdaman

This repository contains the initial _Dockerfile_ for a rasdman only container and the _entrypoint.sh_ bash script that starts rasdaman as a service in the docker container and keeps the container alive.

## Command examples
`
docker run -d -it --rm --name rasdaman local:rasdaman
`

Starts the container with no persistence on docker's volumes

`
docker run -d -it --rm -e RASMGR_HOST_IP="172.17.0.2" --name rasdaman --mount type=bind,src=/host/local/path,dst=/opt/rasdaman/data local:rasdaman
`


Starts the container with a bind volume and RASMGR_HOST_IP environment variable

## Ports

Ports exposed: from 7001 to 7010 (only 7001 mandatory)

## Environment variables

**RASMGR_HOST_IP** substitutes host value in rasmgr.conf with this variable value.

