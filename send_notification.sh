#!/usr/bin/bash

if [[ -z $1 ]]
then
	echo "No message given to send"
	exit -1
fi

curl -d "$1" 'ntfy.sh/stylneo-general'
