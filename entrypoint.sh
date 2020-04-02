#!/bin/bash

# setup correctly /opt/rasdaman/etc/rasmgr.conf
# using RASMGR_HOST_IP environment variable if set
if [ -z $RASMGR_HOST_IP ]; then
  export RASMGR_HOST_IP="localhost" 
fi

# Start rasdaman
$RMANBIN/start_rasdaman.sh

# modifica Roberto Gter
#rm -f $RASMGR_CONF_FILE && sed "s/@hostname@/$RASMGR_HOST_IP/g" /rasmgr.conf.in > $RASMGR_CONF_FILE

if [ -z "$(ls -A $RMANDATA)" ]; then
	$RMANBIN/create_db.sh
fi

# set tomcat9 permissions
chown -R tomcat:tomcat /var/lib/tomcat9
chown -R tomcat:tomcat /var/lib/tomcat9/webapps
chown -R tomcat:tomcat /var/lib/tomcat9/webapps/* 
# Start tomcat
sh -c '/etc/init.d/tomcat9 start 2>&1'

# Start apache2
sh -c 'apache2ctl start 2>&1'

# Verify rasmgr is running
rasmgrnum=`ps aux | grep rasmgr | grep -v grep | wc -l`
rassrvnum=`ps aux | grep rasdaman | grep -v grep | wc -l`

terminate=0

fwirasdatefile='lastfwi'
fwirasdatepath='/opt/rasdaman/scripts'
fwirasdate="$fwirasdatepath"/"$fwirasdatefile"
today=`date "+%Y%m%d"`
fwiimportscript='/opt/rasdaman/scripts/import_container.py'
exechour="06"

while [ true ]; do

  if [ ! -f $fwirasdate ]; then
    /usr/bin/python $fwiimportscript
    echo "$today" > $fwirasdate
  else
    hour=`date "+%H"`
    
    while IFS= read -r lastdate 
    do
      echo ""
    done < $fwirasdate

    if [ "$today" != "$lastdate" ]; then
      if [ "$hour" == "$exechour" ]; then
        /usr/bin/python $fwiimportscript
        echo "$today" > $fwirasdate
      fi
    fi
  fi

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
		sleep 300
	fi
done

# vim: set ts=2 number:

