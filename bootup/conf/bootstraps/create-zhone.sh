#!/bin/bash
# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst
#
# Example NESi REST API server bootstrapping
#
ENDPOINT=http://localhost:5000/nesi/v1

path="`dirname \"$0\"`"

. $path/functions.sh

# Create a network device (admin operation)
req='{
  "vendor": "Zhone",
  "model": "Zhone-Gerät lol",
  "version": "2500",
  "description": "(Juan-)",
  "hostname": "Zhone-Gerät lul",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "uuid": "7777",
  "software_version": "juan"
  }'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Admin user
req='{
  "name": "Admin"
}'

admin_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Admin credentials
req='{
  "username": "admin",
  "password": "secret",
  "user_id": '$admin_id'
}'

admin_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# create a Subrack

req='{
  "name": "1",
  "description": "Juan Zhone"
}'

subrack_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

# create a Card

req='{
  "subrack_id": '$subrack_1',
  "product": "vdsl",
  "description": "Karte von Juan"
}'

card_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

# create a Port

req='{
  "card_id": '$card_1',
  "description": "Network Port 1",
  "admin_state": "1",
  "operational_state": "1",
  "upstream": 4023,
  "downstream": 13232,
  "upstream_max": 8000,
  "downstream_max": 16000
}'

port_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

# create a Port

req='{
  "card_id": '$card_1',
  "description": "Network Port 2",
  "admin_state": "0",
  "operational_state": "0",
  "upstream": 4023,
  "downstream": 13232,
  "upstream_max": 8000,
  "downstream_max": 16000
}'

port_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)