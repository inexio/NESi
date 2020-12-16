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
from experimental.interfaces.api_interface.schemas.cpeports_schemas import CpePortsSchema
from experimental.interfaces.api_interface.views.base_views import *


@app.route(PREFIX + '/boxen/<box_id>/cpe_ports', methods=['GET'])
def show_cpe_ports(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(CpePortsSchema(), 'cpe_ports', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cpe_ports/<id>', methods=['GET'])
def show_cpe_port(box_id, id):
    response = show_component('cpe_ports', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cpe_ports', methods=['POST'])
def new_cpe_port(box_id):
    req = flask.request.json

    '''if 'name' not in req or req['name'] == "":
        cpe = json.loads(show_component(Cpe, box_id, req['cpe_id']).data.decode('utf-8'))
        req['name'] = cpe['name'] + "/" + str(len(cpe['cpe_ports']) + 1)

    response = new_component(CpePortSchema(), CpePort, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/cpe_ports/<id>', methods=['PUT'])
def update_cpe_port(box_id, id):
    req = flask.request.json
    update_component('cpe_ports', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/cpe_ports/<id>', methods=['DELETE'])
def del_cpe_port(box_id, id):
    del_component('cpe_ports', box_id, id)
    return flask.Response(status=204)
