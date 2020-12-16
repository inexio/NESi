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
from experimental.interfaces.api_interface.schemas.credentials_schemas import CredentialsSchema
from experimental.interfaces.api_interface.views.base_views import *



@app.route(PREFIX + '/boxen/<box_id>/credentials', methods=['GET'])
def show_credentials(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(CredentialsSchema(), 'credentials', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/credentials/<id>', methods=['GET'])
def show_credential(box_id, id):
    response = show_component('credentials', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/credentials', methods=['POST'])
def new_credential(box_id):
    req = flask.request.json
    '''response = new_component(CredentialSchema(), Credential, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/credentials/<id>', methods=['DELETE'])
def del_credential(box_id, id):
    del_component('credentials', box_id, id)
    return flask.Response(status=204)
