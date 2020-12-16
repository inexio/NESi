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
from experimental.interfaces.api_interface.schemas.portprofiles_schemas import PortProfilesSchema
from experimental.interfaces.api_interface.views.base_views import *



@app.route(PREFIX + '/boxen/<box_id>/port_profiles', methods=['GET'])
def show_port_profiles(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(PortProfilesSchema(), 'port_profiles', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/port_profiles/<id>', methods=['GET'])
def show_port_profile(box_id, id):
    response = show_component('port_profiles', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/port_profiles', methods=['POST'])
def new_port_profile(box_id):
    req = flask.request.json
    '''response = new_component(PortProfileSchema(), PortProfile, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/port_profiles/<id>', methods=['PUT'])
def update_port_profile(box_id, id):
    req = flask.request.json
    update_component('port_profiles', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/port_profiles/<id>', methods=['DELETE'])
def del_port_profile(box_id, id):
    del_component('port_profiles', box_id, id)
    return flask.Response(status=204)
