#!/bin/bash

# gpg --keyserver keyserver.ubuntu.com --recv-keys 476CF100

current_timestamp=$(date +%y%m%d%H%M%S)
temp_db="/srv/aggreg8streams/${current_timestamp}-simplestreams.db"
db="/srv/aggreg8streams/simplestreams.db"
/home/philroche/.virtualenvs/aggreg8streams/bin/python3 /srv/aggreg8streams/parse_simplestreams.py --database "${temp_db}" --base http://cloud-images.ubuntu.com/releases/streams/v1/index.sjson
/home/philroche/.virtualenvs/aggreg8streams/bin/python3 /srv/aggreg8streams/parse_simplestreams.py --database "${temp_db}" --minimal --append http://cloud-images.ubuntu.com/minimal/releases/streams/v1/index.sjson 

mv --force "${db}" "${db}.rollback"
mv --force "${temp_db}" "${db}"
chown www-data:www-data "${db}.rollback"
chown www-data:www-data "${db}"
supervisorctl restart aggreg8streams8001
