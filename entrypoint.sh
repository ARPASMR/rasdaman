#!/bin/bash

# Start tomcat
sh -c '/etc/init.d/tomcat8 start 2>&1'

# Start apache2
sh -c 'apache2ctl start 2>&1'

RMANHOME=/opt/rasdaman
RMANDATA=$RMANHOME/data
RMANBIN=$RMANHOME/bin
RMANETC=$RMANHOME/etc
RASMGR_CONF_FILE=$RMANETC/rasmgr.conf

# setup correctly /opt/rasdaman/etc/rasmgr.conf
# using RASMGR_HOST_IP environment variable if set
if [ -z $RASMGR_HOST_IP ]; then
	export RASMGR_HOST_IP="localhost" 
fi

# modifica Roberto Gter
#rm -f $RASMGR_CONF_FILE && sed "s/@hostname@/$RASMGR_HOST_IP/g" /rasmgr.conf.in > $RASMGR_CONF_FILE

if [ -z "$(ls -A $RMANDATA)" ]; then
	$RMANBIN/create_db.sh
fi

$RMANBIN/start_rasdaman.sh

# Verify rasmgr is running
rasmgrnum=`ps aux | grep rasmgr | grep -v grep | wc -l`
rassrvnum=`ps aux | grep rasdaman | grep -v grep | wc -l`

terminate=0

while [ true ]; do

	if [ $rasmgrnum = 0 ]; then
		echo "No rasdaman manager process alive. Terminate container."
		terminate=1
	else
		# Verify rasdaman worker processes
		if [ $rassrvnum = 0 ]; then
			echo "No rasdaman worker processes. Terminate container."
			terminate=1
		fi
	fi

	if [ $terminate != 0 ]; then
		break
	else
		sleep 60
	fi
done



