#!/bin/bash

/opt/rasdaman/bin/start_rasdaman.sh

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
