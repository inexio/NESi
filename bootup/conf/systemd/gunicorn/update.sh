#!/bin/bash

rm -rf rm /opt/nesi/venv/lib/python3.6/site-packages/nesi*

cd /opt/nesi/venv/NESi

git pull

python3 -m pip install -r requirements.txt