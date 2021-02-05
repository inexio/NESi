#!/bin/bash

systemctl stop nesi-gunicorn.service

rm /opt/nesi/var/nesi-restapi.db
/opt/nesi/venv/NESi/bootup/./restapi.sh --recreate-db
chown -R nesi.nesi /opt/nesi/var/*

systemctl restart nesi-gunicorn.service