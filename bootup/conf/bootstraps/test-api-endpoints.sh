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
  "vendor": "Alcatel",
  "model": "7360",
  "version": "FX-4",
  "description": "Aclatel Switch",
  "hostname": "Alcatel_7360",
  "mgmt_address": "10.0.0.13",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "uuid": "1"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id

# Create login credentials at the switch (admin operation)
req='{
  "username": "admin",
  "password": "secret"
}'

credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/credentials

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/credentials/$credential_id

# VLAN 1
req='{
  "number": 2620,
  "name": "PPPoE",
  "description": "VLAN access port #1",
  "status": "learned",
  "fdb_id": 2620,
  "role": "access",
  "shutdown": false,
  "mtu": 1495,
  "access_group_in": "",
  "access_group_out": "",
  "ip_redirect": false,
  "ip_proxy_arp": false,
  "unicast_reverse_path_forwarding": false,
  "load_interval": 100,
  "mpls_ip": "10.1.1.12",
  "protocol_filter": "pass-pppoe",
  "pppoe_relay_tag": "configurable",
  "pppoe_linerate": "addactuallinerate",
  "circuit_id_pppoe": "physical-id",
  "remote_id_pppoe": "customer-id"
}'

vlan_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

req='{
    "name": "CPE Management"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/vlans/$vlan_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/vlans

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/vlans/$vlan_id

# PortProfile 1
req='{
  "name": "TEST_DSL_16000",
  "description": "PortProfile #1",
  "type": "service"
}'

port_profile_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/port_profiles

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/port_profiles/$port_profile_id

### Subrack 1/1 ###

# Create a physical subrack at the network device (admin operation)

req='{
  "name": "1/1",
  "description": "Physical subrack #1",
  "planned_type": "rant-a",
  "actual_type": "rant-a",
  "operational_state": "1",
  "admin_state": "1",
  "err_state": "no-error",
  "availability": "available",
  "mode": "no-extended-lt-slots",
  "subrack_class": "main-ethernet",
  "serial_no": "CN1646MAGDGF",
  "variant": "3FE68313CDCDE",
  "ics": "04"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

req='{
    "description": "#1 Physical Subrack"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/subracks/$subrack_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/subracks

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/subracks/$subrack_id

### Card 1 ###

# Create a physical card at the network device (admin operation)

req='{
  "name": "1/1/1",
  "subrack_id": '$subrack_id',
  "description": "Physical card #1",
  "planned_type": "fant-f",
  "actual_type": "fant-f",
  "operational_state": "1",
  "admin_state": "1",
  "err_state": "no-error",
  "availability": "available",
  "alarm_profile": "none",
  "capab_profile": "32port_xDSL",
  "manufacturer": "ALCL",
  "mnemonic": "RDLT-C",
  "pba_code": "3FE68863GGFL",
  "fpba_code": "3FE68863GGFL",
  "fpba_ics": "02",
  "clei_code": "VBIUAALBAB",
  "serial_no": "AA1815FSE1CG",
  "failed_test": "00:00:00:00",
  "lt_restart_time": "1970-01-01:00:00:00",
  "lt_restart_cause": "poweron",
  "lt_restart_num": 0,
  "mgnt_entity_oamipaddr": "0.0.0.0",
  "mgnt_entity_pairnum": 0,
  "dual_host_ip": "0.0.0.0",
  "dual_host_loc": "none",
  "card_type": "eth"
}'

card_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

req='{
    "description": "#1 Physical Card"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/cards/$card_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cards

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cards/$card_id

### Port 1 ###

# Create a physical port at the network device (admin operation)

req='{
  "name": "1/1/1/1",
  "card_id": '$card_id',
  "description": "Physical port #1",
  "operational_state": "0",
  "admin_state": "0",
  "upstream": 0,
  "downstream": 0,
  "upstream_max": 100000,
  "downstream_max": 100000,
  "noise_margin_up": 0,
  "noise_margin_down": 0,
  "tgt_noise_margin_up": 0,
  "tgt_noise_margin_down": 0,
  "attenuation_up": 0,
  "attenuation_down": 0,
  "attained_upstream": 0,
  "attained_downstream": 0,
  "threshold_upstream": 0,
  "threshold_downstream": 0,
  "max_delay_upstream": 0,
  "max_delay_downsteam": 0,
  "if_index": 94502912,
  "type": "ethernet-line",
  "high_speed": 0,
  "connector_present": "not-applicable",
  "media": 0.0,
  "largest_pkt_size": 0,
  "curr_bandwith": 1244000000,
  "phy_addr": " ",
  "last_chg_opr_stat": "352-02:55:19",
  "pkts_unknown_proto": 0,
  "in_octets": 0,
  "out_octets": 0,
  "in_ucast_pkts": 0,
  "out_ucast_pkts": 0,
  "in_mcast_pkts": 0,
  "out_mcast_pkts": 0,
  "in_broadcast_pkts": 0,
  "out_broadcast_pkts": 0,
  "in_discard_pkts": 0,
  "out_discard_pkts": 0,
  "in_err_pkts": 0,
  "out_err_pkts": 0,
  "in_octets_hc": 0,
  "out_octets_hc": 0,
  "in_ucast_pkts_hc": 0,
  "out_ucast_pkts_hc": 0,
  "in_mcast_pkts_hc": 0,
  "out_mcast_pkts_hc": 0,
  "in_broadcast_pkts_hc": 0,
  "out_broadcast_pkts_hc": 0,
  "position": "lt:1/1/1:sfp:2",
  "diag_avail_status": "no-error",
  "los": "not-available",
  "tx_fault": "no-tx-fault",
  "tx_power": "3.85 dBm",
  "rx_power": "not-available",
  "tx_bias_current": "16.17 mA",
  "supply_voltage": "3.23 VDC",
  "temperature": "57.39 degrees Celsius",
  "temperature_tca": "normal-value",
  "voltage_tca": "normal-value",
  "bias_current_tca": "normal-value",
  "tx_power_tca": "normal-value",
  "rx_power_tca": "normal-value",
  "rssi_profile_id": 65535,
  "rssi_state": "enable",
  "inp_up": 0,
  "inp_dn": 0,
  "interl_us": 0,
  "interl_dn": 0,
  "cur_op_mode": "default",
  "rinit_1d": 0,
  "actual_tps_tc_mode": "ptm",
  "rtx_mode_up": "unknown",
  "rtx_mode_dn": "unknown",
  "total_reset_attempt": 0,
  "success_reset_attempt": 0,
  "cur_init_state": "down",
  "shutdown": false,
  "speed": "1G",
  "auto_negotiation": true,
  "mtu": 1495
}'

port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

req='{
    "description": "#1 Physical Port"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/ports/$port_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/ports

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/ports/$port_id

### Ont 1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "name": "1/1/1/1/1",
  "port_id":'$port_id',
  "description": "Ont #1"
}'

ont_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

req='{
    "description": "#1 Ont"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/onts/$ont_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/onts

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/onts/$ont_id

### OntPort 1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "name": "1/1/1/1/1/1/1",
  "ont_id": '$ont_id',
  "description": "OntPort #1"
}'

ont_port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

req='{
    "description": "#1 OntPort"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/ont_ports/$ont_port_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/ont_ports

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/ont_ports/$ont_port_id

### Cpe 1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "name": "1/1/1/1/1/1/1/1",
  "ont_port_id": '$ont_port_id',
  "description": "Cpe #1"
}'

cpe_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

req='{
    "description": "#1 Cpe"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/cpes/$cpe_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cpes

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cpes/$cpe_id

### CpePort 1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "name": "1/1/1/1/1/1/1/1/1",
  "cpe_id": '$cpe_id',
  "description": "CpePort #1"
}'

cpe_port_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

req='{
    "description": "#1 Cpe"
}'

curl -s -d "$req" -H "Content-Type: application/json" -X PUT $ENDPOINT/boxen/$box_id/cpe_ports/$cpe_port_id

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cpe_ports

curl -s -H "Content-Type: application/json" -X GET $ENDPOINT/boxen/$box_id/cpe_ports/$cpe_port_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/cpe_ports/$cpe_port_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/cpes/$cpe_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/ont_ports/$ont_port_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/onts/$ont_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/ports/$port_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/cards/$card_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/subracks/$subrack_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id/credentials/$credential_id

curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/boxen/$box_id