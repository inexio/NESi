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
from ..schemas.route_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/routes', methods=['GET'])
def show_routes(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(RoutesSchema(), Route, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/routes/<id>', methods=['GET'])
def show_route(box_id, id):
    response = show_component(Route, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/routes', methods=['POST'])
def new_route(box_id):
    req = flask.request.json
    response = new_component(RouteSchema(), Route, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/routes/<id>', methods=['DELETE'])
def del_route(box_id, id):
    del_component(Route, box_id, id)
    return flask.Response(status=204)
