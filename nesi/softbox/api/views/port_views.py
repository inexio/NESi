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
from .box_views import show_box
from ..models.card_models import Card
from ..schemas.port_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/ports', methods=['GET'])
def show_ports(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(PortsSchema(), Port, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/ports/<id>', methods=['GET'])
def show_port(box_id, id):
    response = show_component(Port, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/ports', methods=['POST'])
def new_port(box_id):
    req = flask.request.json

    card = json.loads(show_component(Card, box_id, req['card_id']).data.decode('utf-8'))
    box = json.loads(show_box(box_id)[0].data.decode('utf-8'))

    if 'name' not in req or req['name'] == "":
        if box['vendor'] == 'Huawei':
            req['name'] = card['name'] + "/" + str(len(card['ports']))
        else:
            req['name'] = card['name'] + "/" + str(len(card['ports']) + 1)

    if 'position' not in req or req['position'] == "":
        req['position'] = 'lt:' + card['name'] + ':sfp:' + str(len(card['ports']) + 1)

    response = new_component(PortSchema(), Port, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/ports/<id>', methods=['PUT'])
def update_port(box_id, id):
    req = flask.request.json
    update_component(Port, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/ports/<id>', methods=['DELETE'])
def del_port(box_id, id):
    del_component(Port, box_id, id)
    return flask.Response(status=204)
