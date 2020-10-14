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
  "vendor": "KeyMile",
  "model": "MileGate",
  "version": "2500",
  "description": "Example Switch",
  "hostname": "KeyMileMG2500",
  "mgmt_address": "10.0.0.12",
  "software_version": "MG2500V800R016C00",
  "network_protocol": "telnet",
  "network_address": "127.0.0.1",
  "network_port": 9023,
  "uuid": "2500",
  "currTemperature": 15
}'

box_id=$(create_resource "$req" $ENDPOINT/boxen) || exit 1

# Sessionmanager credentials
req='{
  "username": "sessionmanager",
  "password": "secret"
}'

sessionmanager_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Sessionmanager user
req='{
  "name": "sessionmanager",
  "credentials_id": '$sessionmanager_credential_id',
  "level": "Super",
  "profile": "root",
  "append_info": "Sessionmanager",
  "lock_status": "Unlocked"
}'

sessionmanager_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Manager credentials
req='{
  "username": "manager",
  "password": "secret"
}'

manager_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Manager user
req='{
  "name": "manager",
  "credentials_id": '$manager_credential_id',
  "level": "Admin",
  "profile": "admin",
  "append_info": "Manager",
  "lock_status": "Unlocked"
}'

manager_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Maintenance credentials
req='{
  "username": "maintenance",
  "password": "secret"
}'

maintenance_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Manager user
req='{
  "name": "maintenance",
  "credentials_id": '$maintenance_credential_id',
  "level": "Operator",
  "profile": "operator",
  "append_info": "Maintenance",
  "lock_status": "Unlocked"
}'

maintenance_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# Information credentials
req='{
  "username": "information",
  "password": "secret"
}'

information_credential_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/credentials)

# Manager user
req='{
  "name": "information",
  "credentials_id": '$information_credential_id',
  "level": "User",
  "profile": "commonuser",
  "append_info": "Information",
  "lock_status": "Unlocked"
}'

information_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/users)

# test subscriber
req='{
  "name": "tester",
  "number": 9023,
  "type": "unit"
}'

subscriber_id=$(create_resource "$req" $ENDPOINT/boxen/$box_id/subscribers)

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
  "product": "adsl",
  "board_name": "SUAD2",
  "supplier_build_state": "R3D",
  "board_id": "305",
  "hardware_key": 102,
  "software": "suad2_r5c01.esw",
  "software_name": "SUAD2",
  "software_revision": "R5C01",
  "state": "Ok",
  "serial_number": "4363507882",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900030",
  "short_text": "MG SUSE1 SHDSL EFM 32-port",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09862706",
  "manufacturer_build_state": "02",
  "boot_loader": "BLSU1_R1G01/CT23337",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
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

### Chan-1 ###

# Create a logical channel at the network device (admin operation)
req='{
  "port_id": '$port_1_1',
  "description": "Channel #1"
}'

chan_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/channels)

### Interface-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "chan_id": '$chan_1_1_1'
}'

interface_1_1_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/interfaces)

### Unit-2 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "sdsl",
  "board_name": "SUSE1",
  "supplier_build_state": "R1A",
  "board_id": "330",
  "hardware_key": 1,
  "software": "suse1_r4d02_t01.esw",
  "software_name": "SUSE1",
  "software_revision": "R4D02_T01",
  "state": "Ok",
  "serial_number": "6973180458",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900196",
  "short_text": "MG SUAD2 ADSL2+ AnnexB 32-port",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09860762",
  "manufacturer_build_state": "05",
  "boot_loader": "BLSU1_R1F01/CT18388",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_2',
  "admin_state": "1",
  "operational_state": "1"
}'

port_2_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Port-2 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_2',
  "admin_state": "1",
  "operational_state": "1"
}'

port_2_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### LogPort 1 ###

# Create a logical logport object at the network device (admin operation)
req='{
  "card_id": '$unit_2',
  "name": "2/L/2",
  "ports": "ports:2"
}'

logport_2_l_2=$(create_resource "$req" $ENDPOINT/boxen/$box_id/logports)

### Unit-3 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "sdsl",
  "board_name": "SUSE1",
  "supplier_build_state": "R1A",
  "board_id": "330",
  "hardware_key": 3,
  "software": "suse1_r4d02_t01.esw",
  "software_name": "SUSE1",
  "software_revision": "R4D02_T01",
  "state": "Ok",
  "serial_number": "3383369557",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900196",
  "short_text": "MG SUSE1 SHDSL EFM 32-port",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09862706",
  "manufacturer_build_state": "02",
  "boot_loader": "BLSU1_R1G01/CT23337",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_3=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Port-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_3',
  "admin_state": "1",
  "operational_state": "1"
}'

port_3_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/ports)

### Interface-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "port_id": '$port_3_1'
}'

interface_3_1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/interfaces)

### Unit-4 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "adsl",
  "board_name": "SUAD2",
  "supplier_build_state": "R3D",
  "board_id": "305",
  "hardware_key": 104,
  "software": "suad2_r5c01.esw",
  "software_name": "SUAD2",
  "software_revision": "R5C01",
  "state": "Ok",
  "serial_number": "4810312946",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900030",
  "short_text": "MG SUAD2 ADSL2+ AnnexB 32-port",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09860762",
  "manufacturer_build_state": "05",
  "boot_loader": "BLSU1_R1F01/CT18388",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_4=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Unit-5 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "vdsl",
  "board_name": "SUVM4",
  "supplier_build_state": "R1G",
  "board_id": "345",
  "hardware_key": 1,
  "software": "suvm4_r3c02_01.esw",
  "software_name": "SUVM4",
  "software_revision": "R3C02_01",
  "state": "Ok",
  "serial_number": "6702369850",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900293",
  "short_text": "MG SUVM4 VDSL2 ISDN 32-port",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09866094",
  "manufacturer_build_state": "01",
  "boot_loader": "BPSUVM4_R1B03/CT0",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_5=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Unit-6 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "vdsl",
  "board_name": "SUVM6",
  "supplier_build_state": "R1K",
  "board_id": "377",
  "hardware_key": 25,
  "software": "suvm6_r3e10_01.esw",
  "software_name": "SUVM6",
  "software_revision": "R3E10_01",
  "state": "Ok",
  "serial_number": "1283288279",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900528",
  "short_text": "MG SUVM6 VDSL2/17MHz ISDN 48pt",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09869778",
  "manufacturer_build_state": "20",
  "boot_loader": "BPSUVM6_R1B02/CT0",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_6=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Unit-7 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "vdsl",
  "board_name": "SUVM6",
  "supplier_build_state": "R1K",
  "board_id": "377",
  "hardware_key": 14,
  "software": "suvm6_r3e10_01.esw",
  "software_name": "SUVM6",
  "software_revision": "R3E10_01",
  "state": "Ok",
  "serial_number": "6135149854",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900528",
  "short_text": "MG SUVM6 VDSL2/17MHz ISDN 48pt",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09869778",
  "manufacturer_build_state": "20",
  "boot_loader": "BPSUVM6_R1B02/CT0",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_7=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Unit-8 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "vdsl",
  "board_name": "SUVM6",
  "supplier_build_state": "R1K",
  "board_id": "377",
  "hardware_key": 104,
  "software": "suvm6_r3e10_01.esw",
  "software_name": "SUVM6",
  "software_revision": "R3E10_01",
  "state": "Ok",
  "serial_number": "8781619728",
  "manufacturer_name": "KEYMILE",
  "model_name": "37900528",
  "short_text": "MG SUVM6 VDSL2/17MHz ISDN 48pt",
  "manufacturer_id": "100989",
  "manufacturer_part_number": "09869778",
  "manufacturer_build_state": "20",
  "boot_loader": "BPSUVM6_R1B02/CT0",
  "processor": "CPU MPC852T/853T 50MHz, RAM 64MB, FLASH 32MB"
}'

unit_8=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### Unit-19 ###

# Create a physical card at the network device (admin operation)
req='{
  "subrack_id": '$subrack_id',
  "product": "isdn",
  "name": "19"
}'

unit_19=$(create_resource "$req" $ENDPOINT/boxen/$box_id/cards)

### PortGroupPort-1 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_19',
  "admin_state": "1",
  "operational_state": "1",
  "name": "19/G1/1",
  "type": "PSTN"
}'

port_19_G1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/portgroupports)

### PortGroupPort-2 ###

# Create a physical port at the network device (admin operation)
req='{
  "card_id": '$unit_19',
  "admin_state": "1",
  "operational_state": "1",
  "name": "19/G2/1",
  "type": "ISDN"
}'

port_19_G1_1=$(create_resource "$req" $ENDPOINT/boxen/$box_id/portgroupports)