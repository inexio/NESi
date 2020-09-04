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

# PortProfile 1
req='{
  "name": "PPPoe",
  "type": "service",
  "description": "PortProfile #1"
}'

port_profile_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# VLAN 1
req='{
  "number": 2602,
  "name": "VLAN_2602",
  "description": "VLAN #1",
  "type": "smart",
  "attribute": "common",
  "bind_service_profile_id": '$port_profile_id',
  "bind_RAIO_profile_index": "-",
  "priority": "-",
  "state": "up",
  "native_vlan" : "1"
}'

vlan_id1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

### Emu 0 ###

# Create a physical emu at the network device (admin operation)
req='{
  "type": "FAN",
  "number": 0
}'
emu_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/emus)

req='{
  "number": 1
}'
emu_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/emus)

### Emu 0 ###

# Create a physical emu at the network device (admin operation)
req='{
  "type": "H831PMU",
  "number": 2
}'
emu_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/emus)

### Subrack 0 ###

# Create a physical subrack at the network device (admin operation)
req='{
  "name": "0",
  "description": "Physical subrack #1"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

### Card 1 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #1",
  "product": "vdsl",
  "board_name": "H83BVCMM"
}'

card1_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 2 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #2",
  "product": "adsl",
  "board_name": "H83BVCNN"
}'

card2_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 3 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #3",
  "product": "ftth-pon",
  "board_name": "H807GPBH"
}'

card3_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 4 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #4",
  "product": "ftth",
  "board_name": "H831EIUD"
}'

card4_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 5 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #5",
  "product": "ftth",
  "board_name": "H802OPGE"
}'

card5_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 6 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #6",
  "product": "ftth-pon",
  "board_name": "H807GPBH"
}'

card6_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Card 7 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card #7",
  "product": "ftth-pon",
  "board_name": "H807GPBH"
}'

card7_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card1_id',
  "description": "Physical port #1 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated"
}'

port1_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card2_id',
  "description": "Physical port #1 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated"
}'

port2_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)


### PORT 3 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card3_id',
  "description": "Physical port #1 on this card",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "loopback": "disable",
  "admin_state": "deactivated"
}'

port3_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 4 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card4_id',
  "description": "Physical port #1 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated"
}'

port4_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 5 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card5_id',
  "description": "Physical port #1 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated"
}'

port5_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)


### PORT 6 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card5_id',
  "description": "Physical port #2 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated",
  "link": "failed"
}'

port6_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 7 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card6_id',
  "description": "Physical port #7 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated",
  "link": "failed"
}'

port7_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 8 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card7_id',
  "description": "Physical port #8 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated",
  "link": "failed"
}'

port8_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 9 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card7_id',
  "description": "Physical port #9 on this card",
  "loopback": "disable",
  "upstream": 1234,
  "downstream": 4321,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "admin_state": "deactivated",
  "link": "failed"
}'

port9_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont 1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port3_id',
  "description": "Ont #1",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "index": 0
}'

ont_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont 2 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port7_id',
  "description": "Ont #2",
  "index": 0
}'

ont2_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont 3 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port7_id',
  "description": "Ont #3",
  "index": 1
}'

ont3_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont 4 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port7_id',
  "description": "Ont #4",
  "index": 2
}'

ont4_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont 5 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port8_id',
  "description": "Ont #5",
  "index": 0
}'

ont5_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont 6 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port9_id',
  "description": "Ont #6",
  "index": 1
}'

ont7id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_id',
  "ont_port_index": 0,
  "description": "OntPort #1",
  "ont_port_type": "ETH"
}'

ont_port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### OntPort 1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont2_id',
  "ont_port_index": 0,
  "description": "OntPort #2",
  "ont_port_type": "ETH"
}'

ont_port2_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_id',
  "description": "Cpe #1",
  "mac": "8f:db:82:ef:ea:17"
}'

cpe_id1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### Cpe 2 ###

# Create a physical cpe at the vdsl-port (admin operation)

req='{
  "port_id": '$port1_id',
  "description": "Cpe #2",
  "mac": "8f:db:82:ef:ea:17"
}'

cpe_id2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### Cpe 3 ###

# Create a physical cpe at the adsl-port (admin operation)

req='{
  "port_id": '$port2_id',
  "description": "Cpe #3",
  "mac": "8f:db:82:ef:ea:17"
}'

cpe_id3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_id1',
  "description": "CpePort #1"
}'

cpe_port_id1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### CpePort 2 ###

# Create a physical cpe-port at the vdsl-cpe (admin operation)

req='{
  "cpe_id": '$cpe_id2',
  "description": "CpePort #2"
}'

cpe_port_id2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### CpePort 3 ###

# Create a physical cpe-port at the vdsl-cpe (admin operation)

req='{
  "cpe_id": '$cpe_id3',
  "description": "CpePort #3"
}'

cpe_port_id3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### VlanInterface 1 ###

# Create a vlan interface

req='{
  "name": "vlanif2602",
  "vlan_id": '$vlan_id1',
  "admin_state": "UP",
  "line_proto_state": "DOWN",
  "internet_protocol": "enabled",
  "internet_address": "127.0.0.1",
  "subnet_num": "24"
}'

vlan_interface_id1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlan_interfaces)
