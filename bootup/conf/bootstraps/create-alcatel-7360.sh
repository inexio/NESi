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

# relt-a, nelt-b, fglt-b -> ftth cards
# fant-f -> ftth-pon card

#--------------------------------------------------------#
#                                                        #
#   Subrack 1/1                                          #
#   |---> Card 1/1/1 (xdsl)                              #
#   |     |-> Port 1/1/1/1                               #
#   |     |   |-> Cpe 1/1/1/1/1                          #
#   |     |       |-> CpePort 1/1/1/1/1/1                #
#   |     |-> Port 1/1/1/2                               #
#   |     |   |-> Cpe 1/1/1/2/1                          #
#   |     |       |-> CpePort 1/1/1/2/1/1                #
#   |     |-> Port 1/1/1/3                               #
#   |                                                    #
#   |---> Card 1/1/2 (vdsl)                              #
#   |     |-> Port 1/1/2/1                               #
#   |     |   |-> Cpe 1/1/2/1/1                          #
#   |     |       |-> CpePort 1/1/2/1/1/1                #
#   |     |-> Port 1/1/2/2                               #
#   |     |   |-> Cpe 1/1/2/2/1                          #
#   |     |       |-> CpePort 1/1/2/2/1/1                #
#   |     |-> Port 1/1/2/3                               #
#   |                                                    #
#   |---> Card 1/1/3 (adsl)                              #
#   |     |-> Port 1/1/3/1                               #
#   |     |   |-> Cpe 1/1/3/1/1                          #
#   |     |       |-> CpePort 1/1/3/1/1/1                #
#   |     |-> Port 1/1/3/2                               #
#   |     |   |-> Cpe 1/1/3/2/1                          #
#   |     |       |-> CpePort 1/1/3/2/1/1                #
#   |     |-> Port 1/1/3/3                               #
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
  "vendor": "Alcatel",
  "model": "7360",
  "version": "FX-4",
  "description": "Aclatel Switch",
  "hostname": "Alcatel_7360",
  "mgmt_address": "10.0.0.1",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "software_version": "R5.5.02",
  "login_banner": "     ___       __        ______     ___   .___________. _______  __\r\n    /   \\     |  |      /      |   /   \\  |           ||   ____||  |\r\n   /  ^  \\    |  |     |  ,----`  /  ^  \\ `---|  |----`|  |__   |  |\r\n  /  /_\\  \\   |  |     |  |      /  /_\\  \\    |  |     |   __|  |  |\r\n /  _____  \\  |  `----.|  `----./  _____  \\   |  |     |  |____ |  `----.\r\n/__/     \\__\\ |_______| \\______/__/     \\__\\  |__|     |_______||_______|",
  "welcome_banner": "Welcome to Alcatel_7360",
  "uuid": "1"
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Create login credentials at the switch (admin operation)
req='{
  "username": "admin",
  "password": "secret"
}'

admin_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Admin user
req='{
  "name": "admin",
  "credentials_id": '$admin_credential_id'
}'

admin_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# PortProfile 1
req='{
  "name": "TEST_DSL_16000",
  "description": "PortProfile #1",
  "type": "service"
}'

test_dsl_16000_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 2
req='{
  "name": "PSD_036",
  "description": "PortProfile #2",
  "type": "spectrum"
}'

psd_036_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 3
req='{
  "name": "VECT_US_DS",
  "description": "PortProfile #3",
  "type": "vect"
}'

vect_us_ds_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 4
req='{
  "name": "DPBO_3310",
  "description": "PortProfile #4",
  "type": "dpbo"
}'

dpbo_3310_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 5
req='{
  "name": "TEST_FTTH_500M",
  "description": "PortProfile #5",
  "type": "qos",
  "up_policer": "name:50M_CIR",
  "down_policer": "name:500M_CIR",
  "logical_flow_type": "generic"
}'

test_ftth_500m_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 6
req='{
  "name": "TEST_FTTH_1G",
  "description": "PortProfile #6",
  "type": "qos",
  "up_policer": "name:500M_CIR",
  "down_policer": "name:1G_CIR",
  "logical_flow_type": "generic"
}'

test_ftth_1g_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 7
req='{
  "name": "VDSL_VECT_FALLBACK",
  "description": "PortProfile #7",
  "type": "vect"
}'

tvdsl_vect_fallback_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# PortProfile 6
req='{
  "name": "vce-default",
  "description": "Default vce profile",
  "type": "vce"
}'

vce_default_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 1
req='{
  "name": "1G_CIR",
  "description": "Policer #1",
  "type": "policer",
  "committed_info_rate": 1050000,
  "committed_burst_size": 2560000
}'

_1g_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 2
req='{
  "name": "1M_CIR",
  "description": "Policer #2",
  "type": "policer",
  "committed_info_rate": 1050,
  "committed_burst_size": 256000
}'

_1m_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 3
req='{
  "name": "2M_CIR",
  "description": "Policer #3",
  "type": "policer",
  "committed_info_rate": 2100,
  "committed_burst_size": 256000
}'

_2m_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 4
req='{
  "name": "50M_CIR",
  "description": "Policer #4",
  "type": "policer",
  "committed_info_rate": 52500,
  "committed_burst_size": 256000
}'

_50m_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 5
req='{
  "name": "100M_CIR",
  "description": "Policer #5",
  "type": "policer",
  "committed_info_rate": 105000,
  "committed_burst_size": 256000
}'

_100m_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

# Policer 6
req='{
  "name": "500M_CIR",
  "description": "Policer #6",
  "type": "policer",
  "committed_info_rate": 550000,
  "committed_burst_size": 312500
}'

_500m_cir_profile=$(create_resource "$req" $ENDPOINT/boxen/$box_id/port_profiles)

### PPPoE Vlan ###

req='{
  "number": 2620,
  "name": "PPPoE",
  "description": "PPPoE Vlan",
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
  "remote_id_pppoe": "customer-id",
  "in_qos_prof_name": "name:Default_TC0",
  "new_broadcast": "disable",
  "new_secure_fwd": "disable",
  "aging_time": null,
  "dhcp_opt82_ext": "disable"
}'

vlan_pppoe=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

### CPE Management Vlan ###

req='{
  "number": 3320,
  "name": "CPE Management",
  "description": "CPE Management Vlan",
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
  "protocol_filter": null,
  "pppoe_relay_tag": null,
  "pppoe_linerate": null,
  "circuit_id_pppoe": null,
  "remote_id_pppoe": null,
  "circuit_id_dhcp": "physical-id",
  "remote_id_dhcp": "customer-id",
  "in_qos_prof_name": null,
  "new_broadcast": "enable",
  "new_secure_fwd": "enable",
  "aging_time": 21600,
  "dhcp_opt82_ext": "enable"
}'

vlan_cpem=$(create_resource "$req" $ENDPOINT/boxen/$box_id/vlans)

### Subrack 1/1 ###

# Create a physical subrack at the network device (admin operation)

req='{
  "name": "1/1",
  "description": "Physical subrack #1",
  "planned_type": "rvxs-a",
  "actual_type": "rvxs-a",
  "operational_state": "enabled",
  "admin_state": "unlock",
  "err_state": "no-error",
  "availability": "available",
  "mode": "no-extended-lt-slots",
  "subrack_class": "main-ethernet",
  "serial_no": "CN1646MAGDGF",
  "variant": "3FE68313CDCDE",
  "ics": "04"
}'

subrack_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subracks)


### Management Card ###

# Create a physical card at the network device (admin operation)

req='{
  "name": "nt-a",
  "position": "network:0",
  "subrack_id": '$subrack_id',
  "description": "Physical Management card",
  "planned_type": "rant-a",
  "actual_type": "rant-a",
  "operational_state": "enabled",
  "err_state": "no-error",
  "availability": "available",
  "alarm_profile": "none",
  "capab_profile": "not_applicable",
  "manufacturer": "ALCL",
  "mnemonic": "RANT-A",
  "pba_code": "3FE68863GGFL",
  "fpba_code": "3FE68863GGFL",
  "fpba_ics": "03",
  "clei_code": "VAUCAMZKAA",
  "serial_no": "YP1819F4025",
  "failed_test": "00:00:00:00",
  "lt_restart_time": "1970-01-01:00:00:00",
  "lt_restart_cause": "other",
  "lt_restart_num": 0,
  "mgnt_entity_oamipaddr": "0.0.0.0",
  "mgnt_entity_pairnum": 0,
  "dual_host_ip": "0.0.0.0",
  "dual_host_loc": "none"
}'

card_nt_a=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Management Port 1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_nt_a',
  "name": "nt-a:xfp:1",
  "position": "nt-a:xfp:1",
  "description": "Management port #1",
  "operational_state": "up",
  "admin_state": "up",
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

port_mgmt=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort nt-a:xfp:1 ####

req='{
  "connected_id": '$port_mgmt',
  "connected_type": "port",
  "name": "nt-a:xfp:1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)


### Card 1/1/1 ###

# Create a physical card at the network device (admin operation)

req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card 1/1/1",
  "planned_type": "rdlt-c",
  "actual_type": "rdlt-c",
  "operational_state": "enabled",
  "admin_state": "unlock",
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
  "product": "xdsl"
}'

card_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1/1/1/1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_1',
  "description": "Physical port 1/1/1/1",
  "operational_state": "up",
  "admin_state": "up",
  "upstream": 10000,
  "downstream": 25000,
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

port_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/1/1 ####

req='{
  "connected_id": '$port_1_1_1_1',
  "connected_type": "port",
  "name": "1/1/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/1/1  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/1/1  ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### ServicePort 1/1/1/1:1:32 ####

req='{
  "name": "1/1/1/1:1:32",
  "connected_id": '$port_1_1_1_1',
  "connected_type": "port",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_1_1_1_32=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/1/1:1:32  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_1_1_1_32',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_1_1',
  "description": "Cpe 1/1/1/1/1",
  "serial_no": "ABCD123456EF",
  "admin_state": "up",
  "mac": "8f:db:82:ef:ea:17"
}'

cpe_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/1/1/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_1_1_1',
  "description": "CpePort 1/1/1/1/1/1"
}'

cpe_port_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### ServicePort 1/1/1/1/1/1 ####

req='{
  "connected_id": '$cpe_port_1_1_1_1_1_1',
  "connected_type": "cpe",
  "name": "1/1/1/1/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/1/1/1/1  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_1_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/1/1/1/1  ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_1_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Port 1/1/1/2 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_1',
  "description": "Physical port 1/1/1/2",
  "operational_state": "down",
  "admin_state": "up",
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

port_1_1_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/1/2 ####

req='{
  "connected_id": '$port_1_1_1_2',
  "connected_type": "port",
  "name": "1/1/1/1",
  "admin_state": "up",
  "operational_state": "down"
}'

service_port_1_1_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/1/2  ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_1_2',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/1/2  ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_1_2',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/1/2/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_1_2',
  "description": "Cpe 1/1/1/2/1",
  "serial_no": "ABCD654321FE",
  "admin_state": "down",
  "mac": "8d:dc:81:ea:fe:12"
}'

cpe_1_1_1_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/1/1/2/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_1_2_1',
  "description": "CpePort 1/1/1/2/1/1"
}'

cpe_port_1_1_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/1/3 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_1',
  "description": "Physical port 1/1/1/3",
  "operational_state": "down",
  "admin_state": "down",
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

port_1_1_1_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/1/3 ####

req='{
  "connected_id": '$port_1_1_1_3',
  "connected_type": "port",
  "name": "1/1/1/3",
  "admin_state": "down",
  "operational_state": "down"
}'

service_port_1_1_1_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/1/3 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_1_3',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/1/3 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_1_3',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_1'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Card 1/1/2 ###

# Create a physical card at the network device (admin operation)

req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card 1/1/2",
  "planned_type": "rdlt-c",
  "actual_type": "rdlt-c",
  "operational_state": "enabled",
  "admin_state": "unlock",
  "err_state": "no-error",
  "availability": "available",
  "alarm_profile": "none",
  "capab_profile": "32port_xDSL",
  "manufacturer": "ALCL",
  "mnemonic": "FANT-F",
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
  "product": "vdsl"
}'

card_1_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1/1/2/1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_2',
  "description": "Physical port 1/1/2/1",
  "operational_state": "up",
  "admin_state": "up",
  "upstream": 10000,
  "downstream": 25000,
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

port_1_1_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/2/1 ####

req='{
  "connected_id": '$port_1_1_2_1',
  "connected_type": "port",
  "name": "1/1/2/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/2/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_2_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/2/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_2_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/2/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_2_1',
  "description": "Cpe 1/1/2/1/1",
  "serial_no": "GFED123456BA",
  "admin_state": "up",
  "mac": "2a:87:19:09:ae:2f"
}'

cpe_1_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/2/1/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_2_1_1',
  "description": "CpePort 1/1/2/1/1/1"
}'

cpe_port_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/2/2 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_2',
  "description": "Physical port 1/1/2/2",
  "operational_state": "down",
  "admin_state": "up",
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

port_1_1_2_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/2/2 ####

req='{
  "connected_id": '$port_1_1_2_2',
  "connected_type": "port",
  "name": "1/1/2/1",
  "admin_state": "up",
  "operational_state": "down"
}'

service_port_1_1_2_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/2/2 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_2_2',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/2/2 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_2_2',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/2/2/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_2_2',
  "description": "Cpe 1/1/2/2/1",
  "serial_no": "DEFG654321AB",
  "admin_state": "down",
  "mac": "2e:78:09:e6:dc:4e"
}'

cpe_1_1_2_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/2/2/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_2_2_1',
  "description": "CpePort 1/1/2/2/1/1"
}'

cpe_port_1_1_2_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/2/3 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_2',
  "description": "Physical port 1/1/2/3",
  "operational_state": "down",
  "admin_state": "down",
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

port_1_1_2_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/2/3 ####

req='{
  "connected_id": '$port_1_1_2_3',
  "connected_type": "port",
  "name": "1/1/2/3",
  "admin_state": "down",
  "operational_state": "down"
}'

service_port_1_1_2_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/2/3 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_2_3',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/2/3 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_2_3',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_2'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Card 1/1/3 ###

# Create a physical card at the network device (admin operation)

req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card 1/1/3",
  "planned_type": "nant-a",
  "actual_type": "nant-a",
  "operational_state": "enabled",
  "admin_state": "unlock",
  "err_state": "no-error",
  "availability": "available",
  "alarm_profile": "none",
  "capab_profile": "32port_xDSL",
  "manufacturer": "ALCL",
  "mnemonic": "FANT-F",
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
  "product": "adsl"
}'

card_1_1_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1/1/3/1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_3',
  "description": "Physical port 1/1/3/1",
  "operational_state": "up",
  "admin_state": "up",
  "upstream": 10000,
  "downstream": 25000,
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

port_1_1_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/3/1 ####

req='{
  "connected_id": '$port_1_1_3_1',
  "connected_type": "port",
  "name": "1/1/3/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/3/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_3_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/3/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_3_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/3/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_3_1',
  "description": "Cpe 1/1/3/1/1",
  "serial_no": "WXYZ123456BA",
  "admin_state": "up",
  "mac": "fd:28:2e:25:a2:99"
}'

cpe_1_1_3_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/3/1/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_3_1_1',
  "description": "CpePort 1/1/3/1/1/1"
}'

cpe_port_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/3/2 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_3',
  "description": "Physical port 1/1/3/2",
  "operational_state": "down",
  "admin_state": "up",
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

port_1_1_3_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/3/2 ####

req='{
  "connected_id": '$port_1_1_3_2',
  "connected_type": "port",
  "name": "1/1/3/2",
  "admin_state": "up",
  "operational_state": "down"
}'

service_port_1_1_3_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/3/2 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_3_2',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/3/2 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_3_2',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/3/2/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "port_id": '$port_1_1_3_2',
  "description": "Cpe 1/1/3/2/1",
  "serial_no": "DEFG654321AB",
  "admin_state": "down",
  "mac": "c3:3e:81:30:3d:10"
}'

cpe_1_1_3_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/3/2/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_3_2_1',
  "description": "CpePort 1/1/3/2/1/1"
}'

cpe_port_1_1_3_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/3/3 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_3',
  "description": "Physical port 1/1/3/3",
  "operational_state": "down",
  "admin_state": "down",
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

port_1_1_3_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/3/3 ####

req='{
  "connected_id": '$port_1_1_3_3',
  "connected_type": "port",
  "name": "1/1/3/3",
  "admin_state": "down",
  "operational_state": "down"
}'

service_port_1_1_3_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/3/3 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_3_3',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/3/3 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_3_3',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_3'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Card 1/1/4 ###

# Create a physical card at the network device (admin operation)

req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card 1/1/4",
  "planned_type": "relt-a",
  "actual_type": "relt-a",
  "operational_state": "enabled",
  "admin_state": "unlock",
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
  "product": "ftth"
}'

card_1_1_4=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1/1/4/1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_4',
  "description": "Physical port 1/1/4/1",
  "operational_state": "up",
  "admin_state": "up",
  "upstream": 10000,
  "downstream": 25000,
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

port_1_1_4_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/4/1 ####

req='{
  "connected_id": '$port_1_1_4_1',
  "connected_type": "port",
  "name": "1/1/4/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_4_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Ont 1/1/4/1/1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port_1_1_4_1',
  "description": "Ont 1/1/4/1/1",
  "admin_state": "up",
  "index": 1,
  "type": "10gbaselr",
  "basebx10d": "yes",
  "media_available": "available",
  "jabber_state": "jabber",
  "b100basefxfd": "no",
  "b100baselx10": "no",
  "b100basebx10d": "no",
  "b100basebx10u": "yes",
  "b100basetxfd": "yes",
  "b1000basetfd": "no",
  "b10gbasetfd": "yes",
  "b1000basesxfd": "no",
  "b1000baselx10": "no",
  "b1000baselxfd": "yes",
  "b1000basebx10u": "yes",
  "b1000basebx10d": "no",
  "b10gbaser": "no",
  "b10gbaselr": "yes",
  "b10gbaseer": "no",
  "b2500basex": "no",
  "cap100base_tfd": "no",
  "cap1000base_xfd": "yes",
  "cap1000base_tfd": "yes",
  "cap10gbase_tfd": "no",
  "act_num_data_ports": 1,
  "act_num_voice_ports": 0,
  "actual_card_type": "ethernet",
  "actual_ont_integ": "integrated",
  "actual_serial_num": "0168FC3C",
  "actual_version_num": "G2110V1D0",
  "actual_vendorid": "GNXS",
  "actual_cardid": "FiberTwist-G2110",
  "state": "enabled",
  "sernum": "ALCLB140677C"
}'

ont_1_1_4_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1/1/4/1/1/1/1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_4_1_1',
  "description": "OntPort 1/1/4/1/1/1/1",
  "admin_state": "up"
}'

ont_port_1_1_4_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/4/1/1/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_4_1_1_1_1',
  "connected_type": "port",
  "name": "1/1/4/1/1/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_4_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/1/1/1/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_1_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/1/1/1/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_1_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/4/1/1/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_4_1_1_1_1',
  "description": "Cpe 1/1/4/1/1/1/1/1",
  "serial_no": "GFED123456XY",
  "admin_state": "up",
  "mac": "a4:c9:21:bd:11:c3"
}'

cpe_1_1_4_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/4/1/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_4_1_1_1_1_1',
  "description": "CpePort 1/1/4/1/1/1/1/1/1"
}'

cpe_port_1_1_4_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/4/2 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_4',
  "description": "Physical port 1/1/4/2",
  "operational_state": "down",
  "admin_state": "up",
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

port_1_1_4_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/4/2 ####

req='{
  "connected_id": '$port_1_1_4_2',
  "connected_type": "port",
  "name": "1/1/4/2",
  "admin_state": "up",
  "operational_state": "down"
}'

service_port_1_1_4_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/2 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_2',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/2 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_2',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Ont 1/1/4/2/1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port_1_1_4_2',
  "description": "Ont 1/1/4/2/1",
  "admin_state": "up",
  "index": 1,
  "type": "10gbaselr",
  "basebx10d": "yes",
  "media_available": "available",
  "jabber_state": "jabber",
  "b100basefxfd": "no",
  "b100baselx10": "no",
  "b100basebx10d": "no",
  "b100basebx10u": "yes",
  "b100basetxfd": "yes",
  "b1000basetfd": "no",
  "b10gbasetfd": "yes",
  "b1000basesxfd": "no",
  "b1000baselx10": "no",
  "b1000baselxfd": "yes",
  "b1000basebx10u": "yes",
  "b1000basebx10d": "no",
  "b10gbaser": "no",
  "b10gbaselr": "yes",
  "b10gbaseer": "no",
  "b2500basex": "no",
  "auto_neg_supported": true,
  "auto_neg_status": "complete",
  "cap100base_tfd": "no",
  "cap1000base_xfd": "yes",
  "cap1000base_tfd": "yes",
  "cap10gbase_tfd": "no",
  "act_num_data_ports": 1,
  "act_num_voice_ports": 0,
  "actual_card_type": "ethernet",
  "actual_ont_integ": "integrated",
  "actual_serial_num": "0168FC3C",
  "actual_version_num": "G2110V1D0",
  "actual_vendorid": "GNXS",
  "actual_cardid": "FiberTwist-G2110",
  "state": "enabled",
  "sernum": "ALCLB140677C"
}'

ont_1_1_4_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1/1/4/2/1/1/1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_4_2_1',
  "description": "OntPort 1/1/4/2/1/1/1",
  "admin_state": "down"
}'

ont_port_1_1_4_2_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/4/2/1/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_4_2_1_1_1',
  "connected_type": "port",
  "name": "1/1/4/2/1/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_4_2_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/2/1/1/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_2_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/2/1/1/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_2_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/4/2/1/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_4_2_1_1_1',
  "description": "Cpe 1/1/4/2/1/1/1/1",
  "serial_no": "GFED123456YZ",
  "admin_state": "down",
  "mac": "04:1f:1a:14:fc:35"
}'

cpe_1_1_4_2_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/4/2/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_4_2_1_1_1_1',
  "description": "CpePort 1/1/4/2/1/1/1/1/1"
}'

cpe_port_1_1_4_2_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Port 1/1/4/3 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_4',
  "description": "Physical port 1/1/4/3",
  "operational_state": "down",
  "admin_state": "down",
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

port_1_1_4_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/4/3 ####

req='{
  "connected_id": '$port_1_1_4_3',
  "connected_type": "port",
  "name": "1/1/4/2",
  "admin_state": "down",
  "operational_state": "down"
}'

service_port_1_1_4_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/3 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_3',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/3 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_3',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Ont 1/1/4/3/1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port_1_1_4_3',
  "description": "Ont 1/1/4/3/1",
  "admin_state": "down",
  "index": 1,
  "type": "10gbaselr",
  "basebx10d": "yes",
  "media_available": "available",
  "jabber_state": "jabber",
  "b100basefxfd": "no",
  "b100baselx10": "no",
  "b100basebx10d": "no",
  "b100basebx10u": "yes",
  "b100basetxfd": "yes",
  "b1000basetfd": "no",
  "b10gbasetfd": "yes",
  "b1000basesxfd": "no",
  "b1000baselx10": "no",
  "b1000baselxfd": "yes",
  "b1000basebx10u": "yes",
  "b1000basebx10d": "no",
  "b10gbaser": "no",
  "b10gbaselr": "yes",
  "b10gbaseer": "no",
  "b2500basex": "no",
  "auto_neg_supported": true,
  "auto_neg_status": "complete",
  "cap100base_tfd": "no",
  "cap1000base_xfd": "yes",
  "cap1000base_tfd": "yes",
  "cap10gbase_tfd": "no",
  "act_num_data_ports": 1,
  "act_num_voice_ports": 0,
  "actual_card_type": "ethernet",
  "actual_ont_integ": "integrated",
  "actual_serial_num": "0168FC3C",
  "actual_version_num": "G2110V1D0",
  "actual_vendorid": "GNXS",
  "actual_cardid": "FiberTwist-G2110",
  "state": "enabled",
  "sernum": "ALCLB140677C"
}'

ont_1_1_4_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1/1/4/3/1/1/1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_4_3_1',
  "description": "OntPort 1/1/4/3/1/1/1",
  "admin_state": "down"
}'

ont_port_1_1_4_3_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/4/3/1/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_4_3_1_1_1',
  "connected_type": "port",
  "name": "1/1/4/3/1/1/1",
  "admin_state": "down",
  "operational_state": "down"
}'

service_port_1_1_4_3_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/4/3/1/1/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_4_3_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/4/3/1/1/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_4_3_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_4'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/4/3/1/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_4_3_1_1_1',
  "description": "Cpe 1/1/4/3/1/1/1/1",
  "serial_no": "GFED123456WQ",
  "admin_state": "down",
  "mac": "5b:8a:36:50:d4:8b"
}'

cpe_1_1_4_3_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/4/3/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_4_3_1_1_1_1',
  "description": "CpePort 1/1/4/3/1/1/1/1/1"
}'

cpe_port_1_1_4_3_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Card 1/1/5 ###

# Create a physical card at the network device (admin operation)

req='{
  "subrack_id": '$subrack_id',
  "description": "Physical card 1/1/5",
  "planned_type": "fant-f",
  "actual_type": "fant-f",
  "operational_state": "enabled",
  "admin_state": "unlock",
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
  "product": "ftth-pon"
}'

card_1_1_5=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port 1/1/5/1 ###

# Create a physical port at the network device (admin operation)

req='{
  "card_id": '$card_1_1_5',
  "description": "Physical port 1/1/5/1",
  "operational_state": "up",
  "admin_state": "up",
  "upstream": 10000,
  "downstream": 25000,
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

port_1_1_5_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### ServicePort 1/1/5/1 ####

req='{
  "connected_id": '$port_1_1_5_1',
  "connected_type": "port",
  "name": "1/1/5/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_5_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/5/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_5_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/5/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_5_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Ont 1/1/5/1/1 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port_1_1_5_1',
  "description": "Ont 1/1/5/1/1",
  "admin_state": "up",
  "index": 1,
  "type": "10gbaselr",
  "basebx10d": "yes",
  "media_available": "available",
  "jabber_state": "jabber",
  "b100basefxfd": "no",
  "b100baselx10": "no",
  "b100basebx10d": "no",
  "b100basebx10u": "yes",
  "b100basetxfd": "yes",
  "b1000basetfd": "no",
  "b10gbasetfd": "yes",
  "b1000basesxfd": "no",
  "b1000baselx10": "no",
  "b1000baselxfd": "yes",
  "b1000basebx10u": "yes",
  "b1000basebx10d": "no",
  "b10gbaser": "no",
  "b10gbaselr": "yes",
  "b10gbaseer": "no",
  "b2500basex": "no",
  "auto_neg_supported": true,
  "auto_neg_status": "complete",
  "cap100base_tfd": "no",
  "cap1000base_xfd": "yes",
  "cap1000base_tfd": "yes",
  "cap10gbase_tfd": "no",
  "act_num_data_ports": 1,
  "act_num_voice_ports": 0,
  "actual_card_type": "pon",
  "actual_ont_integ": "integrated",
  "actual_serial_num": "0168FC3C",
  "actual_version_num": "G2110V1D0",
  "actual_vendorid": "GNXS",
  "actual_cardid": "FiberTwist-G2110",
  "state": "enabled",
  "sernum": "ALCLB140677C"
}'

ont_1_1_5_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1/1/5/1/1/1/1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_5_1_1',
  "description": "OntPort 1/1/5/1/1/1/1",
  "admin_state": "up"
}'

ont_port_1_1_5_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/5/1/1/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_5_1_1_1_1',
  "connected_type": "ont",
  "name": "1/1/5/1/1/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_5_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/5/1/1/1/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_5_1_1_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/5/1/1/1/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_5_1_1_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/5/1/1/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_5_1_1_1_1',
  "description": "Cpe 1/1/5/1/1/1/1/1",
  "serial_no": "GFED135790XY",
  "admin_state": "up",
  "mac": "29:62:57:a6:60:69"
}'

cpe_1_1_5_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/5/1/1/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_5_1_1_1_1_1',
  "description": "CpePort 1/1/5/1/1/1/1/1/1"
}'

cpe_port_1_1_5_1_1_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### Ont 1/1/5/1/2 ###

# Create a physical ont at the network device (admin operation)

req='{
  "port_id":'$port_1_1_5_1',
  "description": "Ont 1/1/5/1/2",
  "admin_state": "up",
  "index": 1,
  "type": "10gbaselr",
  "basebx10d": "yes",
  "media_available": "available",
  "jabber_state": "jabber",
  "b100basefxfd": "no",
  "b100baselx10": "no",
  "b100basebx10d": "no",
  "b100basebx10u": "yes",
  "b100basetxfd": "yes",
  "b1000basetfd": "no",
  "b10gbasetfd": "yes",
  "b1000basesxfd": "no",
  "b1000baselx10": "no",
  "b1000baselxfd": "yes",
  "b1000basebx10u": "yes",
  "b1000basebx10d": "no",
  "b10gbaser": "no",
  "b10gbaselr": "yes",
  "b10gbaseer": "no",
  "b2500basex": "no",
  "auto_neg_supported": true,
  "auto_neg_status": "complete",
  "cap100base_tfd": "no",
  "cap1000base_xfd": "yes",
  "cap1000base_tfd": "yes",
  "cap10gbase_tfd": "no",
  "act_num_data_ports": 1,
  "act_num_voice_ports": 0,
  "actual_card_type": "pon",
  "actual_ont_integ": "integrated",
  "actual_serial_num": "0168FC3C",
  "actual_version_num": "G2110V1D0",
  "actual_vendorid": "GNXS",
  "actual_cardid": "FiberTwist-G2110",
  "state": "enabled",
  "sernum": "ALCLB140677C"
}'

ont_1_1_5_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/onts)

### OntPort 1/1/5/1/2/1/1 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_5_1_2',
  "description": "OntPort 1/1/5/1/2/1/1",
  "admin_state": "up"
}'

ont_port_1_1_5_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/5/1/2/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_5_1_2_1_1',
  "connected_type": "ont",
  "name": "1/1/5/1/2/1/1",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_5_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/5/1/2/1/1 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_5_1_2_1_1',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/5/1/2/1/1 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_5_1_2_1_1',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/5/1/2/1/1/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_5_1_2_1_1',
  "description": "Cpe 1/1/5/1/2/1/1/1",
  "serial_no": "GFED132546XY",
  "admin_state": "up",
  "mac": "08:97:dc:ca:07:8e"
}'

cpe_1_1_5_1_2_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/5/1/2/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_5_1_2_1_1_1',
  "description": "CpePort 1/1/5/1/2/1/1/1/1"
}'

cpe_port_1_1_5_1_2_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)

### OntPort 1/1/5/1/2/1/2 ###

# Create a physical ont-port at the ont (admin operation)

req='{
  "ont_id": '$ont_1_1_5_1_2',
  "description": "OntPort 1/1/5/1/2/1/2",
  "admin_state": "up"
}'

ont_port_1_1_5_1_2_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ont_ports)

### ServicePort 1/1/5/1/1/1/1 ####

req='{
  "connected_id": '$ont_port_1_1_5_1_2_1_2',
  "connected_type": "ont",
  "name": "1/1/5/1/2/1/2",
  "admin_state": "up",
  "operational_state": "up"
}'

service_port_1_1_5_1_2_1_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_ports)

### Service PPPoE Vlan at ServicePort 1/1/5/1/2/1/2 ###

req='{
  "name": "2620",
  "service_port_id": '$service_port_1_1_5_1_2_1_2',
  "vlan_id": '$vlan_pppoe',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Service CPE Management Vlan at ServicePort 1/1/5/1/2/1/2 ###

req='{
  "name": "3320",
  "service_port_id": '$service_port_1_1_5_1_2_1_2',
  "vlan_id": '$vlan_cpem',
  "card_id": '$card_1_1_5'
}'

service_vlan_=$(create_resource "$req" $ENDPOINT/boxen/$box_id/service_vlans)

### Cpe 1/1/5/1/2/1/2/1 ###

# Create a physical cpe at the ont-port (admin operation)

req='{
  "ont_port_id": '$ont_port_1_1_5_1_2_1_2',
  "description": "Cpe 1/1/5/1/2/1/2/1",
  "serial_no": "GFED213465XY",
  "admin_state": "up",
  "mac": "6f:4a:1e:b4:51:f5"
}'

cpe_1_1_5_1_2_1_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpes)

### CpePort 1/1/5/1/2/1 ###

# Create a physical cpe-port at the cpe (admin operation)

req='{
  "cpe_id": '$cpe_1_1_5_1_2_1_2_1',
  "description": "CpePort 1/1/5/1/2/1/2/1/1"
}'

cpe_port_1_1_5_1_2_1_2_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cpe_ports)