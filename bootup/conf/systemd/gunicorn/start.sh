#!/bin/bash

cd /opt/nesi/venv/

bin/gunicorn --bind "127.0.0.1:5000" --env "NESI_CONFIG=/opt/nesi/etc/nesi.conf" wsgi:app