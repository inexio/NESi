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
from ..models.port_models import Port
from ..models.ontport_models import OntPort
from ..schemas.cpe_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/cpes', methods=['GET'])
def show_cpes(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(CpesSchema(), Cpe, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cpes/<id>', methods=['GET'])
def show_cpe(box_id, id):
    response = show_component(Cpe, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cpes', methods=['POST'])
def new_cpe(box_id):
    req = flask.request.json

    if 'name' not in req or req['name'] == "":
        if 'port_id' in req:
            port = json.loads(show_component(Port, box_id, req['port_id']).data.decode('utf-8'))
            req['name'] = port['name'] + "/" + str(len(port['cpes']) + 1)
        elif 'ont_port_id' in req:
            ont_port = json.loads(show_component(OntPort, box_id, req['ont_port_id']).data.decode('utf-8'))
            req['name'] = ont_port['name'] + "/" + str(len(ont_port['cpes']) + 1)
    if 'port_id' in req and 'ont_port_id' in req:
        raise exceptions.Forbidden('can not have port and ont_port as parent')
    response = new_component(CpeSchema(), Cpe, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/cpes/<id>', methods=['PUT'])
def update_cpe(box_id, id):
    req = flask.request.json
    update_component(Cpe, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/cpes/<id>', methods=['DELETE'])
def del_cpe(box_id, id):
    del_component(Cpe, box_id, id)
    return flask.Response(status=204)
