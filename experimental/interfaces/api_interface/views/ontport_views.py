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
from experimental.interfaces.api_interface.schemas.ontports_schemas import OntPortsSchema
from experimental.interfaces.api_interface.views.base_views import *


@app.route(PREFIX + '/boxen/<box_id>/ont_ports', methods=['GET'])
def show_ont_ports(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(OntPortsSchema(), 'ont_ports', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/ont_ports/<id>', methods=['GET'])
def show_ont_port(box_id, id):
    response = show_component('ont_ports', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/ont_ports', methods=['POST'])
def new_ont_port(box_id):
    req = flask.request.json

    '''if 'name' not in req or req['name'] == "":
        ont = json.loads(show_component(Ont, box_id, req['ont_id']).data.decode('utf-8'))
        box = json.loads(show_box(box_id)[0].data.decode('utf-8'))
        if box['vendor'] == 'Huawei':
            req['name'] = ont['name'] + '/' + str(len(ont['ont_ports']) + 1)
        else:
            req['name'] = ont['name'] + "/1/" + str(len(ont['ont_ports']) + 1)

    port_count = (OntPort.query.filter_by(box_id=box_id, ont_id=req['ont_id']).count())
    if port_count >= 8:
        raise Exception('Cant create more than 8 ont_ports next to ont')
    response = new_component(OntPortSchema(), OntPort, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/ont_ports/<id>', methods=['PUT'])
def update_ont_port(box_id, id):
    req = flask.request.json
    update_component('ont_ports', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/ont_ports/<id>', methods=['DELETE'])
def del_ont_port(box_id, id):
    del_component('ont_ports', box_id, id)
    return flask.Response(status=204)
