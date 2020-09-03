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

USAGE=$(cat << EOF
Usage: $0 [options]
  --help                          Usage help message
  --list_boxen                    List all box instances
  --box-uuid                      Start a box instance in CLI mode
  --daemon                        Start a box instance in daemon mode (ssh or telnet socket)
  --debug                         Start a box with debug mode enabled
EOF
)

uuid=0
list_boxen=false
daemon=false
debug=false

POSITIONAL=()
for arg in "$@"
do
    case $arg in
        --help)
            echo Synopsis: Start a box or list all existing instances
            echo "$USAGE"
            exit 0
            ;;
        --box-uuid)
            uuid=$2
            shift # past argument
            ;;
        --daemon)
            daemon=true
            shift # past argument
            ;;
        --debug)
            debug=true
            shift # past argument
            ;;
        --list-boxen)
            list_boxen=true
            shift # past argument
            ;;
    esac
done

if $list_boxen; then
    python3 ./cli.py --service-root http://127.0.0.1:5000/nesi/v1 --template-root templates/ --list-boxen
elif [ "$uuid" != "" ]; then
    args=''

    if $daemon; then
      args="${args} --daemon"
    fi

    if $debug; then
      args="${args} --debug"
    fi
    python3 ./cli.py --service-root http://127.0.0.1:5000/nesi/v1 --template-root templates/ --box-uuid $uuid $args
fi

