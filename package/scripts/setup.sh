#!/bin/bash
set -e

#Path of solr e.g. /opt/solr
SOLR_PATH=$1

#Logfile e.g. /var/log/solr.log
#LOGFILE=$2

#pid file e.g. /var/run/solr.pid
#PID_FILE=$3

#path containing start.jar file e.g. /opt/solr/latest/server
#START_PATH=$4

if [ ! -d "$SOLR_PATH"]
then
    echo "Creating SOLR_PATH: $SOLR_PATH"
    mkdir -p $SOLR_PATH
fi