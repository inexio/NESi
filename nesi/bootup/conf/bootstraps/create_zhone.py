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
from .function import create_resource
import time


# --------------------------------------------------------#
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
# --------------------------------------------------------#

def create_zhone():
    endpoint = 'http://localhost:5000/nesi/v1'
    time.sleep(1)

    # Create a network device (admin operation)
    req = {
        "vendor": "Zhone",
        "model": "Zhone-Gerät lol",
        "version": "2500",
        "description": "(Juan-)",
        "hostname": "Zhone-Gerät lul",
        "network_protocol": "telnet",
        "network_address": "127.0.0.1",
        "network_port": 9023,
        "uuid": "zhone",
        "software_version": "juan"
    }
    box_id = create_resource(req, (endpoint + '/boxen'))

    # Admin user
    req = {
        "name": "Admin"
    }
    admin_id = create_resource(req, (endpoint + '/boxen/' + box_id + '/users'))

    # Admin credentials
    req = {
        "username": "admin",
        "password": "secret",
        "user_id": admin_id
    }
    admin_credential_id = create_resource(req, (endpoint + '/boxen/' + box_id + '/credentials'))

    # create a Subrack
    req = {
        "name": "1",
        "description": "Juan Zhone"
    }
    subrack_1 = create_resource(req, (endpoint + '/boxen/' + box_id + '/subracks'))

    # create a Card
    req = {
        "subrack_id": subrack_1,
        "product": "vdsl",
        "description": "Karte von Juan"
    }
    card_1 = create_resource(req, (endpoint + '/boxen/' + box_id + '/cards'))

    # create a Port
    req = {
        "card_id": card_1,
        "description": "Network Port 1",
        "admin_state": "1",
        "operational_state": "1",
        "upstream": 4023,
        "downstream": 13232,
        "upstream_max": 8000,
        "downstream_max": 16000
    }
    port_1 = create_resource(req, (endpoint + '/boxen/' + box_id + '/ports'))

    # create a Port
    req = {
        "card_id": card_1,
        "description": "Network Port 2",
        "admin_state": "0",
        "operational_state": "0",
        "upstream": 4023,
        "downstream": 13232,
        "upstream_max": 8000,
        "downstream_max": 16000
    }
    port_2 = create_resource(req, (endpoint + '/boxen/' + box_id + '/ports'))
    return
