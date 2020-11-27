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

# Initial cleanup of vendors table
curl -s -H "Content-Type: application/json" -X DELETE $ENDPOINT/vendors

# ----------------------------------------------------------------------- Alcatel ----------------------------------------------------------------------- #

req='{
    "name": "Alcatel"
}'

vendor_id=$(create_resource "$req" $ENDPOINT/vendors)

req='{
    "name": "7360",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "FX-4",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "FX-8",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "7330",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "1",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "7356",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "1",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "7363",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "1",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

# ----------------------------------------------------------------------- HUAWEI ----------------------------------------------------------------------- #

req='{
    "name": "Huawei"
}'

vendor_id=$(create_resource "$req" $ENDPOINT/vendors)

req='{
    "name": "5603",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "T",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "5606",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "T",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "5608",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "T",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "5616",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "1",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "5622",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "A",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "5623",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "A",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

# ----------------------------------------------------------------------- PBN ----------------------------------------------------------------------- #

req='{
    "name": "PBN"
}'

vendor_id=$(create_resource "$req" $ENDPOINT/vendors)

req='{
    "name": "AOCM3608-2x10GE",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "EPON OLT",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "AOCM3956",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "Ethernet Switch",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "AOCM3924",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "Ethernet Switch",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)

req='{
    "name": "AOCM3948",
    "vendor_id": '$vendor_id'
}'

model_id=$(create_resource "$req" $ENDPOINT/models)

req='{
    "name": "Ethernet Switch",
    "model_id": '$model_id'
}'

version_id=$(create_resource "$req" $ENDPOINT/versions)