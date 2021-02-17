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
from ..models.port_models import Port
from ..schemas.ont_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/onts', methods=['GET'])
def show_onts(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(OntsSchema(), Ont, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/onts/<id>', methods=['GET'])
def show_ont(box_id, id):
    response = show_component(Ont, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/onts', methods=['POST'])
def new_ont(box_id):
    req = flask.request.json

    if 'name' not in req or req['name'] == "":
        port = json.loads(show_component(Port, box_id, req['port_id']).data.decode('utf-8'))
        box = json.loads(show_box(box_id)[0].data.decode('utf-8'))
        if box['vendor'] == 'Huawei':
            req['name'] = port['name'] + "/" + str(len(port['onts']))
        else:
            req['name'] = port['name'] + "/" + str(len(port['onts']) + 1)

    response = new_component(OntSchema(), Ont, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/onts/<id>', methods=['PUT'])
def update_ont(box_id, id):
    req = flask.request.json
    update_component(Ont, req, box_id, id)

    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/onts/<id>', methods=['DELETE'])
def del_ont(box_id, id):
    del_component(Ont, box_id, id)
    return flask.Response(status=204)
