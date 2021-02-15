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
from ..schemas.vlan_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/vlans', methods=['GET'])
def show_vlans(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(VlansSchema(), Vlan, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/vlans/<id>', methods=['GET'])
def show_vlan(box_id, id):
    response = show_component(Vlan, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/vlans', methods=['POST'])
def new_vlan(box_id):
    req = flask.request.json
    response = new_component(VlanSchema(), Vlan, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/vlans/<id>', methods=['PUT'])
def update_vlan(box_id, id):
    req = flask.request.json
    update_component(Vlan, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/vlans/<id>', methods=['DELETE'])
def del_vlan(box_id, id):
    del_component(Vlan, box_id, id)
    return flask.Response(status=204)
