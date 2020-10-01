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
from ..schemas.channel_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/channels', methods=['GET'])
def show_channels(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(ChannelsSchema(), Channel, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/channels/<id>', methods=['GET'])
def show_channel(box_id, id):
    response = show_component(Channel, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/channels', methods=['POST'])
def new_channel(box_id):
    req = flask.request.json

    if 'name' not in req or req['name'] == "":
        if 'port_id' in req:
            port = json.loads(show_component(Port, box_id, req['port_id']).data.decode('utf-8'))
            req['name'] = port['name'] + "/" + str(len(port['channels']) + 1)
    response = new_component(ChannelSchema(), Channel, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/channels/<id>', methods=['PUT'])
def update_channel(box_id, id):
    req = flask.request.json
    update_component(Channel, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/channels/<id>', methods=['DELETE'])
def del_channel(box_id, id):
    del_component(Channel, box_id, id)
    return flask.Response(status=204)
