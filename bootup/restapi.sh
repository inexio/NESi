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

#!/bin/bash
#
# Invoke CLI simulator REST API server and issue a series of REST API
# calls to create an example network device (box).
#
# Fail the entire script on any failure.
#

set -e

RESTAPI_CONF=$(mktemp /tmp/nesi.XXXXXX)

USAGE=$(cat << EOF
Usage: $0 [options]
  --help                          Usage help message
  --recreate-db                   Populate REST API DB with some data
  --keep-running                  Keep REST API servers running
  --debug                         Start REST API with debug mode enabled
  --alcatel-api-build             Start REST API with Alcatel specific data
  --test-alcatel-commands         Start Alcatel test environment
  --huawei-api-build              Start REST API with Huawei specific data
  --test-huawei-commands          Start Huawei test environment
  --keymile-api-build             Start REST API with Keymile specific data
  --test-keymile-commands         Start Keymile test environment
  --edgecore-api-build            Start REST API with Edgecore specific data
  --test-edgcore-commands         Start Edgecore test environment
  --pbn-api-build                 Start REST API with Pbn specific data
  --test-pbn-commands             Start Pbn test environment
  --zhone-api-build               Start REST API with Zhone specific data
  --test-zhone-commands           Start Zhone test environment
EOF
)


recreate_db=no
alcatel_api=no
alcatel_commands=no
huawei_api=no
huawei_commands=no
edgecore_api=no
edgecore_commands=no
zhone_api=no
zhone_commands=no
pbn_api=no
pbn_commands=no
keymile_api=no
keymile_commands=no
keep_running=no
debug=no

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        --help)
            echo Synopsis: invoke REST API servers, optionally initialize
            echo the underlying DB.
            echo "$USAGE"
            exit 0
            ;;
        --recreate-db)
            recreate_db=yes
            shift # past argument
            ;;
        --keep-running)
            keep_running=yes
            shift # past argument
            ;;
        --debug)
            debug=yes
            shift # past argument
            ;;
        --alcatel-api-build)
            alcatel_api=yes
            shift # past argument
            ;;
        --huawei-api-build)
            huawei_api=yes
            shift # past argument
            ;;
        --keymile-api-build)
            keymile_api=yes
            shift # past argument
            ;;
        --edgecore-api-build)
            edgecore_api=yes
            shift # past argument
            ;;
        --pbn-api-build)
            pbn_api=yes
            shift # past argument
            ;;
        --zhone-api-build)
            zhone_api=yes
            shift # past argument
            ;;
        --test-alcatel-commands)
            alcatel_api=yes
            alcatel_commands=yes
            shift # past argument
            ;;
        --test-huawei-commands)
            huawei_api=yes
            huawei_commands=yes
            shift # past argument
            ;;
        --test-keymile-commands)
            keymile_api=yes
            keymile_commands=yes
            shift # past argument
            ;;
        --test-edgecore-commands)
            edgecore_api=yes
            edgecore_commands=yes
            shift # past argument
            ;;
        --test-pbn-commands)
            pbn_api=yes
            pbn_commands=yes
            shift # past argument
            ;;
        --test-zhone-commands)
            zhone_api=yes
            zhone_commands=yes
            shift # past argument
            ;;
        *)
          echo Invalid argument
          exit 1
    esac
done

sed -e 's/DEBUG = True/DEBUG = False/g' $(pwd)/bootup/conf/nesi.conf > $RESTAPI_CONF

args=''

if [ $debug = "yes" ]; then
    args="${args} --debug"
fi

if [ $recreate_db = "yes" ] || [ $alcatel_api = "yes" ] || [ $huawei_api = "yes" ] || [ $keymile_api = "yes" ] || [ $edgecore_api = "yes" ] || [ $pbn_api = "yes" ] || [ $zhone_api = "yes" ]; then
    python3 api.py \
        --config $RESTAPI_CONF \
        --recreate-db $args
fi

python3 api.py \
    --config $RESTAPI_CONF $args &

RESTAPI_PID=$!

function cleanup()
{
    rm -fr  $RESTAPI_CONF
    kill $RESTAPI_PID && true
}

trap cleanup EXIT

echo Waiting for dust to settle down...

sleep 5

bash bootup/conf/bootstraps/create-vendors-and-models.sh

if [ $recreate_db = "yes" ]; then
    #bash bootup/conf/bootstraps/create-box-port-vlan.sh
    #bash bootup/conf/bootstraps/create-alcatel-7360.sh
    #bash bootup/conf/bootstraps/create-huawei-5623.sh
    bash bootup/conf/bootstraps/create-keymile-MG2200.sh
fi

if [ $alcatel_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-alcatel-7360.sh
fi
if [ $huawei_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-huawei-5623.sh
fi
if [ $keymile_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-keymile-MG2200.sh #work_in_progress
fi
if [ $edgecore_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-alcatel-7360.sh #work_in_progress
fi
if [ $pbn_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-alcatel-7360.sh #work_in_progress
fi
if [ $zhone_api = "yes" ]; then
    bash bootup/conf/bootstraps/create-alcatel-7360.sh #work_in_progress
fi


if [ $alcatel_commands = "yes" ]; then
    python3 ./cli.py  --test "Alcatel"
fi
if [ $huawei_commands = "yes" ]; then
    python3 ./cli.py  --test "Huawei"
fi
if [ $keymile_commands = "yes" ]; then
    python3 ./cli.py  --test "Keymile"
fi
if [ $edgecore_commands = "yes" ]; then
    python3 ./cli.py  --test "Edgecore"
fi
if [ $pbn_commands = "yes" ]; then
    python3 ./cli.py  --test "Pbn"
fi
if [ $zhone_commands = "yes" ]; then
    python3 ./cli.py  --test "Zhone"
fi

if [ $keep_running = "yes" ]; then
    cat -
fi

exit 0
