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
  "vendor": "PBN",
  "model": "AOCM3924",
  "version": "Ethernet Switch",
  "description": "PBN Switch",
  "hostname": "PBN_Switch",
  "mgmt_address": "10.0.0.1",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "software_version": "",
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

### VLAN 3220 ###
# Create a logical vlan at the network device
req='{
  "name": "3220",
  "number": 3220,
  "description": "Vlan 3220",
  "role": "access",
  "type": "DYNAMIC",
  "mac_address": "bd9f.d3e4.9f18"
}'

vlan_3220_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

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
  "operational_state": "1",
  "spanning_tree_guard_root": true,
  "switchport_trunk_vlan_allowed": "3220",
  "switchport_mode_trunk": true,
  "switchport_pvid": 3220,
  "no_lldp_transmit": true,
  "pbn_speed": 3,
  "switchport_block_multicast": true,
  "switchport_rate_limit_egress": 3,
  "switchport_rate_limit_ingress": 5,
  "no_pdp_enable": true,
  "no_snmp_trap_link_status": true,
  "exclamation_mark": true
}'

port_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Serviceport 0/1 ###

req='{
  "name": "0/1",
  "connected_id": '$port_0_1',
  "connected_type": "port",
  "admin_state": "1",
  "operational_state": "1"
}'

service_port_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service Vlan 3220 at ServicePort 0/1  ###

req='{
  "name": "3220",
  "service_port_id": '$service_port_0_1',
  "vlan_id": '$vlan_3220_id',
  "card_id": '$card_0'
}'

service_vlan_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Port 2 ###

# Create a physical card at the network device (admin operation)
req='{
  "name": "0/2",
  "card_id": '$card_0',
  "description": "Port #2",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 1 ###

# Create a physical card at the network device (admin operation)
req='{
  "product": "ftth-pon",
  "subrack_id": '$subrack_id',
  "description": "Card #1"
}'

card_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1 ###

# Create a physical card at the network device (admin operation)
req='{
  "name": "1/1",
  "card_id": '$card_1',
  "description": "Port #1",
  "admin_state": "1",
  "operational_state": "1",
  "spanning_tree_guard_root": true,
  "switchport_trunk_vlan_allowed": "3220",
  "switchport_mode_trunk": true,
  "switchport_pvid": 3220,
  "no_lldp_transmit": true,
  "pbn_speed": 3,
  "switchport_block_multicast": true,
  "switchport_rate_limit_egress": 3,
  "switchport_rate_limit_ingress": 5,
  "no_pdp_enable": true,
  "no_snmp_trap_link_status": true,
  "exclamation_mark": true,
  "switchport_protected": 3
}'

port_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Serviceport 1/1 ###

req='{
  "name": "1/1",
  "connected_id": '$port_1_1',
  "connected_type": "port",
  "admin_state": "1",
  "operational_state": "1"
}'

service_port_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service Vlan 3220 at ServicePort 1/1  ###

req='{
  "name": "3220",
  "service_port_id": '$service_port_1_1',
  "vlan_id": '$vlan_3220_id',
  "card_id": '$card_1'
}'

service_vlan_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Ont 1/1:1 ###

req='{
  "name": "1/1/1",
  "description": "Ont 1/1:1",
  "admin_state": "1",
  "operational_state": "1",
  "port_id": '$port_1_1',
  "mac_address": "ea03.6cc5.7488"
}'
ont_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### Ont Port 1/1:1/1 ###

req='{
  "name": "1/1/1/1",
  "description": "OntPort 1/1:1/1",
  "ont_id": '$ont_1_1_1',
  "operational_state": "0",
  "admin_state": "0",
  "flow_control": "Disable",
  "duplex": "Auto-Duplex",
  "speed": "Auto-Speed",
  "storm_control": "Disable"
}'
ont_port_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)
