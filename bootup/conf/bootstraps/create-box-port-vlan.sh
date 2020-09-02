#!/bin/bash
#
# Example NESi REST API server bootstrapping
#
ENDPOINT=http://localhost:5000/nesi/v1

path="`dirname \"$0\"`"

. $path/functions.sh

# Create a network device (admin operation)
req='{
  "vendor": "Test",
  "model": "7361",
  "version": "FX-69",
  "description": "Test Switch",
  "hostname": "Test_7361",
  "mgmt_address": "10.0.0.13"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Create login credentials at the switch (admin operation)
req='{
  "username": "admin",
  "password": "secret"
}'

credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

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

### Subrack 1/1 ###

# Create a physical subrack at the network device (admin operation)

req='{
  "name": "1/1",
  "description": "Physical subrack #1",
  "planned_type": "rant-a",
  "actual_type": "rant-a",
  "operational_state": "enabled",
  "admin_state": "unlock",
  "err_state": "no-error",
  "availability": "available",
  "mode": "no-extended-lt-slots",
  "subrack_class": "main-ethernet",
  "serial_no": "CN1646MADVGF",
  "variant": "3FE68313CCDEA",
  "ics": "04"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)

