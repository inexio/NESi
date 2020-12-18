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
#   |---> Card 0/1   (vdsl)                              #
#   |     |-> Port 0/1/0                                 #
#   |     |   |-> Cpe 0/1/0 1                            #
#   |     |       |-> CpePort 0/1/0 1/1                  #
#   |     |-> Port 0/1/1                                 #
#   |     |   |-> Cpe 0/1/1 1                            #
#   |     |       |-> CpePort 0/1/1 1/1                  #
#   |     |-> Port 0/1/2                                 #
#   |                                                    #
#   |---> Card 0/2   (adsl)                              #
#   |     |-> Port 0/2/0                                 #
#   |     |   |-> Cpe 0/2/0 1                            #
#   |     |       |-> CpePort 0/2/0 1/1                  #
#   |     |-> Port 0/2/1                                 #
#   |     |   |-> Cpe 0/2/1 1                            #
#   |     |       |-> CpePort 0/2/1 1/1                  #
#   |     |-> Port 0/2/2                                 #
#   |                                                    #
#   |---> Card 0/3   (ftth)                              #
#   |     |-> Port 0/3/0                                 #
#   |     |   |-> Ont 0/3/0 0                            #
#   |     |       |-> OntPort 0/3/0 0/1                  #
#   |     |           |-> Cpe 0/3/0 0/1 1                #
#   |     |               |-> CpePort 0/3/0 0/1 1/1      #
#   |     |-> Port 0/3/1                                 #
#   |     |   |-> Ont 0/3/1 0                            #
#   |     |       |-> OntPort 0/3/1 0/1                  #
#   |     |           |-> Cpe 0/3/1 0/1 1                #
#   |     |               |-> CpePort 0/3/1 0/1 1/1      #
#   |     |-> Port 0/3/2                                 #
#   |     |   |-> Ont 0/3/2 0                            #
#   |     |       |-> OntPort 0/3/2 0/1                  #
#   |     |-> Port 0/3/3                                 #
#   |     |   |-> Ont 0/3/3 0                            #
#   |     |       |-> OntPort 0/3/3 0/1                  #
#   |     |           |-> Cpe 0/3/3 0/1 1                #
#   |     |               |-> CpePort 0/3/3 0/1 1/1      #
#   |     |-> Port 0/3/4                                 #
#   |         |-> Ont 0/3/4 0                            #
#   |             |-> OntPort 0/3/4 0/1                  #
#   |                 |-> Cpe 0/3/4 0/1 1                #
#   |                     |-> CpePort 0/3/4 0/1 1/1      #
#   |                                                    #
#   |---> Card 0/4   (ftth-pon)                          #
#   |     |-> Port 0/4/0                                 #
#   |         |-> Ont 0/4/0 0                            #
#   |         |   |-> OntPort 0/4/0 0/1                  #
#   |         |       |-> Cpe 0/4/0 0/1 1                #
#   |         |           |-> CpePort 0/4/0 0/1 1/1      #
#   |         |-> Ont 0/4/0 1                            #
#   |             |-> OntPort 0/4/0 1/1                  #
#   |             |   |-> Cpe 0/4/0 1/1 1                #
#   |             |       |-> CpePort 0/4/0 1/1 1/1      #
#   |             |-> OntPort 0/4/0 1/2                  #
#   |                 |-> Cpe 0/4/0 1/2 1                #
#   |                     |-> CpePort 0/4/0 1/2 1/1      #
#   |                                                    #
#   |---> Card 0/5   (ftth)                              #
#   |     |-> Port 0/5/0                                 #
#   |     |   |-> Ont 0/5/0 0                            #
#   |     |       |-> OntPort 0/5/0 0/1                  #
#   |     |           |-> Cpe 0/5/0 0/1 1                #
#   |     |               |-> CpePort 0/5/0 0/1 1/1      #
#   |     |-> Port 0/5/1                                 #
#   |     |   |-> Ont 0/5/1 0                            #
#   |     |       |-> OntPort 0/5/1 0/1                  #
#   |     |           |-> Cpe 0/5/1 0/1 1                #
#   |     |               |-> CpePort 0/5/1 0/1 1/1      #
#   |     |-> Port 0/5/2                                 #
#   |     |   |-> Ont 0/5/2 0                            #
#   |     |       |-> OntPort 0/5/2 0/1                  #
#   |     |-> Port 0/5/3                                 #
#   |     |   |-> Ont 0/5/3 0                            #
#   |     |       |-> OntPort 0/5/3 0/1                  #
#   |     |           |-> Cpe 0/5/3 0/1 1                #
#   |     |               |-> CpePort 0/5/3 0/1 1/1      #
#   |     |-> Port 0/5/4                                 #
#   |         |-> Ont 0/5/4 0                            #
#   |             |-> OntPort 0/5/4 0/1                  #
#   |                 |-> Cpe 0/5/4 0/1 1                #
#   |                     |-> CpePort 0/5/4 0/1 1/1      #
#--------------------------------------------------------#

# Create a network device (admin operation)
req='{
  "vendor": "Huawei",
  "model": "5623",
  "version": "A",
  "description": "Huawei 5623A box",
  "hostname": "Huawei_5623A",
  "mgmt_address": "10.0.0.12",
  "software_version": "MA5623V800R016C00",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "dsl_mode": "tr165",
  "uuid": "5623"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Super Admin user
req='{
  "name": "Root",
  "level": "Super",
  "profile": "root",
  "append_info": "Super Admin",
  "reenter_num": 3,
  "reenter_num_temp": 3,
  "lock_status": "unlocked"
}'

root_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Super Admin credentials
req='{
  "username": "root",
  "password": "secret",
  "user_id": '$root_id'
}'

root_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Service Profile
req='{
  "name": "line_spectrum_1",
  "type": "service",
  "description": "Service Profile",
  "l0_time": 255,
  "l2_time": 30,
  "l3_time": 255,
  "max_transmite_power_reduction": 3,
  "total_max_power_reduction": 9,
  "bit_swap_ds": 1,
  "bit_swap_us": 1,
  "allow_transitions_to_idle": 2,
  "allow_transitions_to_lowpower": 2,
  "reference_clock": "FreeRun",
  "force_inp_ds": 1,
  "force_inp_us": 1,
  "g_993_2_profile": 12,
  "mode_specific": "enable",
  "T1_413": "enable",
  "G_992_1": "enable",
  "G_992_2": "enable",
  "G_992_3": "enable",
  "G_992_4": "enable",
  "G_992_5": "enable",
  "AnnexB_G_993_2": "enable",
  "us0_psd_mask": 32
}'

line_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Service Profile
req='{
  "name": "PPPoE",
  "type": "service",
  "description": "Service Profile"
}'

service_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PPPoE Vlan
req='{
  "number": 2620,
  "name": "PPPoE",
  "description": "The standard PPPoE Vlan",
  "type": "smart",
  "attribute": "common",
  "bind_service_profile_id": '$service_profile',
  "priority": "-",
  "native_vlan" : "1"
}'

vlan_pppoe=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

### VlanInterface 1 ###

# Create a vlan interface

req='{
  "name": "vlanif2620",
  "vlan_id": '$vlan_pppoe',
  "admin_state": "1",
  "line_proto_state": "1",
  "internet_protocol": "enabled",
  "internet_address": "127.0.0.1",
  "subnet_num": "24"
}'

vlan_interface_pppoe=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlan_interfaces)

# CPE Management Vlan
req='{
  "number": 3320,
  "name": "CPE Management",
  "description": "The standard CPE Management Vlan",
  "type": "smart",
  "attribute": "common",
  "priority": "-",
  "native_vlan" : "1"
}'

vlan_cpem=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

### Fan Emu ###

# Create a physical emu at the network device (admin operation)
req='{
  "type": "FAN",
  "number": 0
}'
emu_fan=$(create_resource "$req" $ENDPOINT/boxen/$box_id/emus)

### Emu 2 ###

# Create a physical emu at the network device (admin operation)
req='{
  "type": "H831PMU",
  "number": 2
}'
emu2_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/emus)

### Subrack 0 ###

# Create a physical subrack at the network device (admin operation)
req='{
  "name": "0",
  "description": "Physical subrack 0"
}'

subrack_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

### Management Card 0/0 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/0",
  "product": "mgnt",
  "board_name": "HS22CCVW",
  "board_status": "Active_normal"
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
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1",
  "combo_status": "-",
  "optic_status": "normal",
  "mdi": "-",
  "speed_h": "auto_1000",
  "duplex": "auto_full",
  "flow_ctrl": "off",
  "active_state": "active",
  "link": "online",
  "alm_prof_15_min" : "-",
  "warn_prof_15_min": "-",
  "alm_prof_24_hour": "-",
  "warn_prof_24_hour": "-"
}'

port_0_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### PORT 0/0/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_0',
  "description": "Physical port 0/0/1",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1",
  "combo_status": "-",
  "optic_status": "normal",
  "mdi": "-",
  "speed_h": "auto_1000",
  "duplex": "auto_full",
  "flow_ctrl": "off",
  "active_state": "active",
  "link": "online",
  "alm_prof_15_min" : "-",
  "warn_prof_15_min": "-",
  "alm_prof_24_hour": "-",
  "warn_prof_24_hour": "-"
}'

port_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 0/1 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/1",
  "product": "vdsl",
  "board_name": "H80DSDPM"
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
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Serviceport 0 ###

req='{
  "name": "0",
  "connected_id": '$port_0_1_0',
  "connected_type": "port",
  "admin_state": "1",
  "operational_state": "1"
}'

service_port_0_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 0  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_0_1_0',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_0_1'
}'

service_vlan_0_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe at port 0/1/0 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_1_0',
  "description": "Cpe 0/1/0 1",
  "mac": "03ed-5da1-4d5d",
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
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Cpe at port 0/1/1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_1_1',
  "description": "Cpe 0/1/1 1",
  "mac": "8e1c-0205-a3dc",
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
  "card_id": '$card_0_1',
  "description": "Physical port 0/1/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 0/2 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/2",
  "product": "adsl",
  "board_name": "H83BVCNN"
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
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_2_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Cpe at port 0/2/0 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_2_0',
  "description": "Cpe 0/2/0 1",
  "mac": "6126-5ceb-8aa6",
  "admin_state": "1"
}'

cpe_0_2_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_2_0_1',
  "description": "CpePort 0/2/0 1/1"
}'

cpe_port_0_2_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/2/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/2/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Cpe at port 0/2/1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "port_id": '$port_0_2_1',
  "description": "Cpe 0/2/1 1",
  "mac": "49a6-2391-f47b",
  "admin_state": "0"
}'

cpe_0_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_2_1_1',
  "description": "CpePort 0/2/1 1/1"
}'

cpe_port_0_2_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/2/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_2',
  "description": "Physical port 0/2/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_2_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Card 0/3 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/3",
  "product": "ftth",
  "board_name": "H831EIUD"
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
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_3_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/3/0 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_3_0',
  "description": "Ont 0/3/0 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_3_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/3/0 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_3_0_0',
  "ont_port_index": 0,
  "description": "0/3/0 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_3_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/3/0 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_3_0_0_1',
  "description": "Cpe 0/3/0 0/1 1",
  "admin_state": "1",
  "mac": "a710-053f-5796"
}'

cpe_0_3_0_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/3/0 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_3_0_0_1_1',
  "description": "CpePort 0/3/0 0/1 1/1"
}'

cpe_port_0_3_0_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/3/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_3',
  "description": "Physical port 0/3/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/3/1 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_3_1',
  "description": "Ont 0/3/1 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0
}'

ont_0_3_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/3/1 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_3_1_0',
  "ont_port_index": 0,
  "description": "0/3/1 0/1",
  "operational_state": "0",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_3_1_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/3/1 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_3_1_0_1',
  "description": "Cpe 0/3/1 0/1 1",
  "admin_state": "0",
  "mac": "d43f-3def-d99a"
}'

cpe_0_3_1_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/3/1 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_3_1_0_1_1',
  "description": "CpePort 0/3/1 0/1 1/1"
}'

cpe_port_0_3_1_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/3/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_3',
  "description": "Physical port 0/3/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_3_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/3/2 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_3_2',
  "description": "Ont 0/3/2 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_3_2_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/3/2 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_3_2_0',
  "ont_port_index": 0,
  "description": "0/3/2 0/1",
  "operational_state": "0",
  "admin_state": "0",
  "ont_port_type": "ETH"
}'

ont_port_0_3_2_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### PORT 0/3/3 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_3',
  "description": "Physical port 0/3/3",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_3_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/3/3 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_3_3',
  "description": "Ont 0/3/3 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_3_3_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/3/3 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_3_3_0',
  "ont_port_index": 0,
  "description": "0/3/3 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_3_3_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/3/3 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_3_3_0_1',
  "description": "Cpe 0/3/3 0/1 1",
  "admin_state": "1",
  "mac": "e8a0-c51e-8adc"
}'

cpe_0_3_3_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/3/3 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_3_3_0_1_1',
  "description": "CpePort 0/3/3 0/1 1/1"
}'

cpe_port_0_3_3_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/3/4 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_3',
  "description": "Physical port 0/3/4",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1",
  "speed_h": "100"
}'

port_0_3_4=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/3/4 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_3_4',
  "description": "Ont 0/3/4 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_3_4_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/3/4 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_3_4_0',
  "ont_port_index": 0,
  "description": "0/3/4 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_3_4_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/3/4 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_3_4_0_1',
  "description": "Cpe 0/3/4 0/1 1",
  "admin_state": "1",
  "mac": "b2b5-e273-7860"
}'

cpe_0_3_4_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/3/4 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_3_4_0_1_1',
  "description": "CpePort 0/3/4 0/1 1/1"
}'

cpe_port_0_3_4_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Card 0/4 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/4",
  "product": "ftth-pon",
  "board_name": "H807GPBH"
}'

card_0_4=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/4/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_4',
  "description": "Physical port 0/4/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_4_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/4/0 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_4_0',
  "description": "Ont 0/4/0 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0
}'

ont_0_4_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/4/0 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_4_0_0',
  "ont_port_index": 0,
  "description": "0/4/0 0/1",
  "operational_state": "0",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_4_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/4/0 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_4_0_0_1',
  "description": "Cpe 0/4/0 0/1 1",
  "admin_state": "0",
  "mac": "7b80-9599-6590"
}'

cpe_0_4_0_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/4/0 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_4_0_0_1_1',
  "description": "CpePort 0/4/0 0/1 1/1"
}'

cpe_port_0_4_0_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Ont at port 0/4/0 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_4_0',
  "description": "Ont 0/4/0 1",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "0",
  "admin_state": "1",
  "index": 1
}'

ont_0_4_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/4/0 1/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_4_0_1',
  "ont_port_index": 0,
  "description": "0/4/0 1/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_4_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Serviceport 1 ###

req='{
  "name": "1",
  "connected_id": '$ont_port_0_4_0_1_1',
  "connected_type": "ont",
  "admin_state": "1",
  "operational_state": "1"
}'

service_port_0_4_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_0_4_0_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_0_4'
}'

service_vlan_0_4_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 0/4/0 1/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_4_0_1_1',
  "description": "Cpe 0/4/0 1/1 1",
  "admin_state": "1",
  "mac": "261b-9d83-545a"
}'

cpe_0_4_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/4/0 1/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_4_0_1_1_1',
  "description": "CpePort 0/4/0 1/1 1/1"
}'

cpe_port_0_4_0_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Serviceport 2 ###

req='{
  "name": "2",
  "connected_id": '$cpe_port_0_4_0_1_1_1_1',
  "connected_type": "cpe",
  "admin_state": "1",
  "operational_state": "1"
}'

service_port_0_4_0_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 2  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_0_4_0_1_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_0_4'
}'

service_vlan_0_4_0_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### OntPort 0/4/0 1/2 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_4_0_1',
  "ont_port_index": 0,
  "description": "0/4/0 1/2",
  "operational_state": "0",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_4_0_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/4/0 1/2 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_4_0_1_2',
  "description": "Cpe 0/4/0 1/2 1",
  "admin_state": "0",
  "mac": "261b-9d83-545a"
}'

cpe_0_4_0_1_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/4/0 1/2 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_4_0_1_2_1',
  "description": "CpePort 0/4/0 1/2 1/1"
}'

cpe_port_0_4_0_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Card 0/5 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_0',
  "description": "Physical card 0/5",
  "product": "ftth",
  "board_name": "H802OPGE"
}'

card_0_5=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PORT 0/5/0 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_5',
  "description": "Physical port 0/5/0",
  "loopback": "disable",
  "upstream": 10000,
  "downstream": 25000,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_5_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/5/0 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_5_0',
  "description": "Ont 0/5/0 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0
}'

ont_0_5_0_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/5/0 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_5_0_0',
  "ont_port_index": 0,
  "description": "0/5/0 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_5_0_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/5/0 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_5_0_0_1',
  "description": "Cpe 0/5/0 0/1 1",
  "admin_state": "1",
  "mac": "0cdb-be79-2528"
}'

cpe_0_5_0_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/5/0 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_5_0_0_1_1',
  "description": "CpePort 0/5/0 0/1 1/1"
}'

cpe_port_0_5_0_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/5/1 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_5',
  "description": "Physical port 0/5/1",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "0"
}'

port_0_5_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/5/1 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_5_1',
  "description": "Ont 0/5/1 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0
}'

ont_0_5_1_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/5/1 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_5_1_0',
  "ont_port_index": 0,
  "description": "0/5/1 0/1",
  "operational_state": "0",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_5_1_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/5/1 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_5_1_0_1',
  "description": "Cpe 0/5/1 0/1 1",
  "admin_state": "0",
  "mac": "c8cd-656b-7110"
}'

cpe_0_5_1_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/5/1 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_5_1_0_1_1',
  "description": "CpePort 0/5/1 0/1 1/1"
}'

cpe_port_0_5_1_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/5/2 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_5',
  "description": "Physical port 0/5/2",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "0",
  "operational_state": "0"
}'

port_0_5_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/4/2 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_5_2',
  "description": "Ont 0/5/2 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "0",
  "admin_state": "0",
  "index": 0
}'

ont_0_5_2_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/5/2 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_5_2_0',
  "ont_port_index": 0,
  "description": "0/5/2 0/1",
  "operational_state": "0",
  "admin_state": "0",
  "ont_port_type": "ETH"
}'

ont_port_0_5_2_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### PORT 0/5/3 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_5',
  "description": "Physical port 0/5/3",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_5_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/5/3 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_5_3',
  "description": "Ont 0/5/3 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_5_3_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/5/3 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_5_3_0',
  "ont_port_index": 0,
  "description": "0/5/3 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_5_3_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/5/3 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_5_3_0_1',
  "description": "Cpe 0/5/3 0/1 1",
  "admin_state": "1",
  "mac": "e8a0-c51e-8adc"
}'

cpe_0_5_3_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/5/3 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_5_3_0_1_1',
  "description": "CpePort 0/5/3 0/1 1/1"
}'

cpe_port_0_5_4_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### PORT 0/5/4 and deps ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$card_0_5',
  "description": "Physical port 0/5/4",
  "loopback": "disable",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": "100000",
  "downstream_max": "100000",
  "admin_state": "1",
  "operational_state": "1"
}'

port_0_5_4=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Ont at port 0/5/4 ###

# Create a physical ont at the network device (admin operation)
req='{
  "port_id":'$port_0_5_4',
  "description": "Ont 0/5/4 0",
  "memory_occupation": "50%",
  "cpu_occupation": "1%",
  "operational_state": "1",
  "admin_state": "1",
  "index": 0,
  "vendor_id": "HWTC",
  "version": "535.B",
  "software_version": "V3R025C29D195"
}'

ont_0_5_4_0=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 0/5/4 0/1 ###

# Create a physical ont-port at the ont (admin operation)
req='{
  "ont_id": '$ont_0_5_4_0',
  "ont_port_index": 0,
  "description": "0/5/4 0/1",
  "operational_state": "1",
  "admin_state": "1",
  "ont_port_type": "ETH"
}'

ont_port_0_5_4_0_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### Cpe 0/5/4 0/1 1 ###

# Create a physical cpe at the ont-port (admin operation)
req='{
  "ont_port_id": '$ont_port_0_5_4_0_1',
  "description": "Cpe 0/5/4 0/1 1",
  "admin_state": "1",
  "mac": "444c-8a1a-7596"
}'

cpe_0_5_4_0_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 0/5/4 0/1 1/1 ###

# Create a physical cpe-port at the cpe (admin operation)
req='{
  "cpe_id": '$cpe_0_5_4_0_1_1',
  "description": "CpePort 0/4/4 0/1 1/1"
}'

cpe_port_0_5_4_0_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)
