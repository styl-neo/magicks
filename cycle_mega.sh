#!/bin/bash

getDate(){
	if [ -z "$1" ]
	then
		echo [$(date +"%R:%S")]
	else
		echo [$(date +"%R:%S" -d "$1")]
	fi
}

while true 
do
	mspid=$(pidof megasync)
	if [ ! -z "$mspid" ] 
	then
		echo "$(getDate) Killing MEGASync with pid of $mspid";
		kill $mspid;
		echo "$(getDate) Sleeping until $(getDate '+75 minutes')";
		sleep 75m;
	fi;
	echo "$(getDate) Starting MEGASync";
	megasync &
	echo "$(getDate) Sleeping until $(getDate '+15 minutes')";
	sleep 15m;
done;


