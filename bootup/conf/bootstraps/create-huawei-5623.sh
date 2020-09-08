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
#   |---> Card 0/0   (vdsl)                              #
#   |     |-> Port 0/0/0                                 #
#   |     |   |-> Cpe 0/0/0 1                            #
#   |     |       |-> CpePort 0/0/0 1/1                  #
#   |     |-> Port 0/0/1                                 #
#   |     |   |-> Cpe 0/0/1 1                            #
#   |     |       |-> CpePort 0/0/1 1/1                  #
#   |     |-> Port 0/0/2                                 #
#   |                                                    #
#   |---> Card 0/1   (adsl)                              #
#   |     |-> Port 0/1/0                                 #
#   |     |   |-> Cpe 0/1/0 1                            #
#   |     |       |-> CpePort 0/1/0 1/1                  #
#   |     |-> Port 0/1/1                                 #
#   |     |   |-> Cpe 0/1/1 1                            #
#   |     |       |-> CpePort 0/1/1 1/1                  #
#   |     |-> Port 0/1/2                                 #
#   |                                                    #
#   |---> Card 0/2   (ftth)                              #
#   |     |-> Port 0/2/0                                 #
#   |     |   |-> Ont                           #
#   |     |       |-> OntPort               #
#   |     |           |-> Cpe             #
#   |     |               |-> CpePort   #
#   |     |-> Port 0/2/1                                 #
#   |     |   |-> Ont                           #
#   |     |       |-> OntPort               #
#   |     |           |-> Cpe             #
#   |     |               |-> CpePort   #
#   |     |-> Port 0/2/2                                 #
#   |                                                    #
#   |---> Card 0/3   (ftth-pon)                          #
#         |-> Port 0/3/0                                 #
#             |-> Ont                           #
#             |   |-> OntPort               #
#             |       |-> Cpe             #
#             |           |-> CpePort   #
#             |-> Ont                           #
#                 |-> OntPort               #
#                 |   |-> Cpe             #
#                 |       |-> CpePort   #
#                 |-> OntPort               #
#                     |-> Cpe             #
#                         |-> CpePort   #
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

### Cpe at port 0/0/0 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_0_0',
  "description": "Cpe 0/0/0 1",
  "mac": "03:ed:5d:a1:4d:5d",
  "admin_state": "1"
}'

cpe_0_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_0_0_1',
  "description": "CpePort 0/0/0 1/1"
}'

cpe_port_0_0_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

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

### Cpe at port 0/0/1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_0_1',
  "description": "Cpe 0/0/1 1",
  "mac": "8e:1c:02:05:a3:dc",
  "admin_state": "0"
}'

cpe_0_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_0_1_1',
  "description": "CpePort 0/0/1 1/1"
}'

cpe_port_0_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

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

port_0_0_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

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

### Cpe at port 0/1/0 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_1_0',
  "description": "Cpe 0/1/0 1",
  "mac": "61:26:5c:eb:8a:a6",
  "admin_state": "1"
}'

cpe_0_1_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_1_0_1',
  "description": "CpePort 0/1/0 1/1"
}'

cpe_port_0_1_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

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

### Cpe at port 0/1/1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_1_1',
  "description": "Cpe 0/1/1 1",
  "mac": "49:a6:23:91:f4:7b",
  "admin_state": "0"
}'

cpe_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_1_1_1',
  "description": "CpePort 0/1/1 1/1"
}'

cpe_port_0_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

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

### Card 0/3 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/3",
  "product": "ftth-pon",
  "board_name": "H807GPBH"
}'

card_0_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/3/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_3',
  "description": "Physical port 0/3/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_3_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/3/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/3/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/3/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/3/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_3_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)
