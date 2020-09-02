#!/bin/bash
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