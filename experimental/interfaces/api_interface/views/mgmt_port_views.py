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

from .box_views import show_box
from experimental.interfaces.api_interface.views.config_views import app, PREFIX, flask
from experimental.interfaces.api_interface.schemas.mgmt_ports_schemas import MgmtPortsSchema
from experimental.interfaces.api_interface.views.base_views import *


@app.route(PREFIX + '/boxen/<box_id>/mgmt_ports', methods=['GET'])
def show_mgmt_ports(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(MgmtPortsSchema(), 'mgmt_ports', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/mgmt_ports/<id>', methods=['GET'])
def show_mgmt_port(box_id, id):
    response = show_component('mgmt_ports', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/mgmt_ports', methods=['POST'])
def new_mgmt_port(box_id):
    req = flask.request.json

    '''mgmt_card = json.loads(show_component(MgmtCard, box_id, req['mgmt_card_id']).data.decode('utf-8'))
    box = json.loads(show_box(box_id)[0].data.decode('utf-8'))

    if 'name' not in req or req['name'] == "": #TODO evtl. noch zu bearbeiten
        if box['vendor'] == 'Huawei':
            req['name'] = mgmt_card['name'] + "/" + str(len(mgmt_card['mgmt_ports']))
        else:
            req['name'] = mgmt_card['name'] + "/" + str(len(mgmt_card['mgmt_ports']) + 1)

    response = new_component(MgmtPortSchema(), MgmtPort, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/mgmt_ports/<id>', methods=['PUT'])
def update_mgmt_port(box_id, id):
    req = flask.request.json
    update_component('mgmt_ports', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/mgmt_ports/<id>', methods=['DELETE'])
def del_mgmt_port(box_id, id):
    del_component('mgmt_ports', box_id, id)
    return flask.Response(status=204)
