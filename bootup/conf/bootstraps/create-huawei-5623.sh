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
#   Subrack 1/1                                          #
#   |---> Card 1/1/1 (vdsl)                              #
#   |     |-> Port 1/1/1/1                               #
#   |     |   |-> Cpe 1/1/1/1/1                          #
#   |     |       |-> CpePort 1/1/1/1/1/1                #
#   |     |-> Port 1/1/1/2                               #
#   |     |   |-> Cpe 1/1/1/2/1                          #
#   |     |       |-> CpePort 1/1/1/2/1/1                #
#   |     |-> Port 1/1/1/3                               #
#   |                                                    #
#   |---> Card 1/1/2 (adsl)                              #
#   |     |-> Port 1/1/2/1                               #
#   |     |   |-> Cpe 1/1/2/1/1                          #
#   |     |       |-> CpePort 1/1/2/1/1/1                #
#   |     |-> Port 1/1/2/2                               #
#   |     |   |-> Cpe 1/1/2/2/1                          #
#   |     |       |-> CpePort 1/1/2/2/1/1                #
#   |     |-> Port 1/1/2/3                               #
#   |                                                    #
#   |---> Card 1/1/4 (ftth)                              #
#   |     |-> Port 1/1/4/1                               #
#   |     |   |-> Ont 1/1/4/1/1                          #
#   |     |       |-> OntPort 1/1/4/1/1/1/1              #
#   |     |           |-> Cpe 1/1/4/1/1/1/1/1            #
#   |     |               |-> CpePort 1/1/4/1/1/1/1/1/1  #
#   |     |-> Port 1/1/4/2                               #
#   |     |   |-> Ont 1/1/4/2/1                          #
#   |     |       |-> OntPort 1/1/4/2/1/1/1              #
#   |     |           |-> Cpe 1/1/4/2/1/1/1/1            #
#   |     |               |-> CpePort 1/1/4/2/1/1/1/1/1  #
#   |     |-> Port 1/1/4/3                               #
#   |                                                    #
#   |---> Card 1/1/5 (ftth-pon)                          #
#         |-> Port 1/1/5/1                               #
#             |-> Ont 1/1/5/1/1                          #
#             |   |-> OntPort 1/1/5/1/1/1/1              #
#             |       |-> Cpe 1/1/5/1/1/1/1/1            #
#             |           |-> CpePort 1/1/5/1/1/1/1/1/1  #
#             |-> Ont 1/1/5/1/2                          #
#                 |-> OntPort 1/1/5/1/2/1/1              #
#                 |   |-> Cpe 1/1/5/1/2/1/1/1            #
#                 |       |-> CpePort 1/1/5/1/2/1/1/1/1  #
#                 |-> OntPort 1/1/5/1/2/1/2              #
#                     |-> Cpe 1/1/5/1/2/1/2/1            #
#                         |-> CpePort 1/1/5/1/2/1/2/1/1  #
#                                                        #
#--------------------------------------------------------#

# Create a network device (admin operation)
req='{
  "vendor": "Huawei",
  "model": "5623",
  "version": "A",
  "description": "Example Switch",
  "hostname": "Huawei_5623A",
  "mgmt_address": "10.0.0.12",
  "software_version": "MA5623V800R016C00",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "uuid": "5623"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Super Admin credentials
req='{
  "username": "root",
  "password": "secret"
}'

root_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Super Admin user
req='{
  "name": "root",
  "credentials_id": '$root_credential_id',
  "level": "Super",
  "profile": "root",
  "append_info": "Super Admin",
  "reenter_num": 3,
  "reenter_num_temp": 3,
  "lock_status": "Unlocked"
}'

root_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

### Subrack 0 ###

# Create a physical subrack at the network device (admin operation)
req='{
  "name": "0",
  "description": "Physical subrack 0"
}'

subrack_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

### Card 0/0 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/0",
  "product": "vdsl",
  "board_name": "H83BVCMM"
}'

card_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/0/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_0',
  "description": "Physical port 0/0/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/0/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_0',
  "description": "Physical port 0/0/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/0/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_0',
  "description": "Physical port 0/0/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_0_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 0/1 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/1",
  "product": "adsl",
  "board_name": "H83BVCNN"
}'

card_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/1/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_1',
  "description": "Physical port 0/1/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/1/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_1',
  "description": "Physical port 0/1/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/1/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_0',
  "description": "Physical port 0/1/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 0/2 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/2",
  "product": "ftth",
  "board_name": "H831EIUD"
}'

card_0_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/2/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/2/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_2_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/2/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/2/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/2/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/2/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

