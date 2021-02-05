#!/bin/bash

systemctl stop nesi.service

rm /tmp/nesi-restapi.db
/opt/nesi/NESi/bootup/./restapi.sh --recreate-db

systemctl restart nesi.service