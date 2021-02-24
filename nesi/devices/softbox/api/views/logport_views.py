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
from ..schemas.logport_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/logports', methods=['GET'])
def show_logports(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(LogPortsSchema(), LogPort, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/logports/<id>', methods=['GET'])
def show_logport(box_id, id):
    response = show_component(LogPort, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/logports', methods=['POST'])
def new_logport(box_id):
    req = flask.request.json
    response = new_component(LogPortSchema(), LogPort, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/logports/<id>', methods=['PUT'])
def update_logport(box_id, id):
    req = flask.request.json
    update_component(LogPort, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/logports/<id>', methods=['DELETE'])
def del_logport(box_id, id):
    del_component(LogPort, box_id, id)
    return flask.Response(status=204)
