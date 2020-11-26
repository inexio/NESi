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

#--------------------------------------------------------#
#                                                        #
#   Subrack 0                                            #
#   |---> Card 1                                         #
#   |     |-> Port 1/1                                   #
#   |     |   |-> Interface 1/1                          #
#                                                        #
#--------------------------------------------------------#
#                                                        #
#   default Vlan 1                                       #
#   Enable Credentials                                   #
#   Backup Credentials                                   #
#                                                        #
#--------------------------------------------------------#

# Create a network device (admin operation)
req='{
  "vendor": "EdgeCore",
  "model": "ECS4120-28Fv2-I",
  "version": "A",
  "description": "EdgeCore ECS4120-28Fv2-I box",
  "hostname": "ed-ge-co-re-1",
  "mgmt_address": "10.0.0.12",
  "software_version": "MA5623V800R016C00",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "dsl_mode": "tr165",
  "uuid": "1111"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Admin user
req='{
  "name": "Admin",
  "profile": "root"
}'

admin_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Admin credentials
req='{
  "username": "admin",
  "password": "secret",
  "user_id": '$admin_id'
}'

admin_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# enable user
req='{
  "name": "Enable",
  "profile": "enable"
}'

enable_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Super enable credentials
req='{
  "username": "enable",
  "password": "enable",
  "user_id": '$enable_id'
}'

enable_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# backup user
req='{
  "name": "Backuo",
  "profile": "backup"
}'

backup_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Super backup credentials
req='{
  "username": "backup",
  "password": "backup",
  "user_id": '$backup_id'
}'

backup_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

### Subrack 0 ###

# Create a physical subrack at the network device (admin operation)
req='{
  "name": "",
  "description": "Pseudo Subrack"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

### Unit-1 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "name": "1",
  "product": "adsl"
}'

unit_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_1',
  "admin_state": "1",
  "operational_state": "1"
}'

port_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Interface-1 ###

# Create a physical interface at the network device (admin operation)
req='{
  "port_id": '$port_1_1'
}'

interface_3_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/interfaces)

# default Vlan
req='{
  "number": 1,
  "name": "default",
  "description": "The standard Vlan"
}'

vlan_pppoe=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)