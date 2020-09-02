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

from .base_views import *
from ..schemas.vlan_interface_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/vlan_interfaces', methods=['GET'])
def show_vlan_interfaces(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(VlanInterfacesSchema(), VlanInterface, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/vlan_interfaces/<id>', methods=['GET'])
def show_vlan_interface(box_id, id):
    response = show_component(VlanInterface, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/vlan_interfaces', methods=['POST'])
def new_vlan_interface(box_id):
    req = flask.request.json
    response = new_component(VlanInterfaceSchema(), VlanInterface, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/vlan_interfaces/<id>', methods=['PUT'])
def update_vlan_interface(box_id, id):
    req = flask.request.json
    update_component(VlanInterface, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/vlan_interfaces/<id>', methods=['DELETE'])
def del_vlan_interface(box_id, id):
    del_component(VlanInterface, box_id, id)
    return flask.Response(status=204)
