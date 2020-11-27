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
  "vendor": "PBN",
  "model": "AOCM3924",
  "version": "Ethernet Switch",
  "description": "PBN Switch",
  "hostname": "PBN_TEST",
  "mgmt_address": "10.0.0.1",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "software_version": "?",
  "uuid": "pbn"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Create login user
req='{
  "name": "Standard Login",
  "status": "offline",
  "lock_status": "unlocked",
  "level": "Admin",
  "profile": "admin"
}'

login_user_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Create login credentials at the switch (admin operation)
req='{
  "username": "admin",
  "password": "secret",
  "user_id": '$login_user_id'
}'

credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Create enable user
req='{
  "name": "Enable",
  "status": "offline",
  "lock_status": "unlocked",
  "level": "Enable",
  "profile": "enable"
}'

ena_user_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Create enable credentials at the switch
req='{
  "username": "ena",
  "password": "ena-secret",
  "user_id": '$ena_user_id'
}'

ena_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

### Subrack 0 ###

# Create a physical subrack at the network device (admin operation)
req='{
  "name": "",
  "description": "Pseudo Subrack"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

### Card 0 ###

# Create a physical card at the network device (admin operation)
req='{
  "product": "ftth",
  "subrack_id": '$subrack_id',
  "description": "Card #0"
}'

card_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1 ###

# Create a physical card at the network device (admin operation)
req='{
  "name": "0/1",
  "card_id": '$card_0',
  "description": "Port #1",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)