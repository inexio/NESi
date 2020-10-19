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

from .base_views import *
from ..schemas.srvc_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/srvcs', methods=['GET'])
def show_srvcs(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(SrvcsSchema(), Srvc, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/srvcs/<id>', methods=['GET'])
def show_srvc(box_id, id):
    response = show_component(Srvc, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/srvcs/<id>', methods=['PUT'])
def update_srvc(box_id, id):
    req = flask.request.json
    update_component(Srvc, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/srvcs', methods=['POST'])
def new_srvc(box_id):
    req = flask.request.json
    response = new_component(SrvcSchema(), Srvc, req, box_id)
    return response, 201

@app.route(PREFIX + '/boxen/<box_id>/srvcs/<id>', methods=['DELETE'])
def del_srvc(box_id, id):
    del_component(Srvc, box_id, id)
    return flask.Response(status=204)
