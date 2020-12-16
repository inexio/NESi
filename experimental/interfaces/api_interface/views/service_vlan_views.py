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

from experimental.interfaces.api_interface.views.config_views import app, PREFIX, flask
from experimental.interfaces.api_interface.schemas.service_vlans_schemas import ServiceVlansSchema
from experimental.interfaces.api_interface.views.base_views import *


@app.route(PREFIX + '/boxen/<box_id>/service_vlans', methods=['GET'])
def show_service_vlans(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(ServiceVlansSchema(), 'servicevlans', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/service_vlans/<id>', methods=['GET'])
def show_service_vlan(box_id, id):
    response = show_component('servicevlans', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/service_vlans/<id>', methods=['PUT'])
def update_service_vlan(box_id, id):
    req = flask.request.json
    update_component('servicevlans', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/service_vlans', methods=['POST'])
def new_service_vlan(box_id):
    req = flask.request.json
    '''response = new_component(ServiceVlanSchema(), ServiceVlan, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/service_vlans/<id>', methods=['DELETE'])
def del_service_vlan(box_id, id):
    del_component('servicevlans', box_id, id)
    return flask.Response(status=204)
