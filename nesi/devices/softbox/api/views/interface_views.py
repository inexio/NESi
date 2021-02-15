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
from ..models.channel_models import Channel
from ..models.logport_models import LogPort
from ..schemas.interface_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/interfaces', methods=['GET'])
def show_interfaces(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(InterfacesSchema(), Interface, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/interfaces/<id>', methods=['GET'])
def show_interface(box_id, id):
    response = show_component(Interface, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/interfaces', methods=['POST'])
def new_interface(box_id):
    req = flask.request.json
    box = json.loads(show_box(box_id)[0].data.decode('utf-8'))

    if 'name' not in req or req['name'] == "":
        if box['vendor'] == 'KeyMile':
            if 'port_id' in req:
                port = json.loads(show_component(Port, box_id, req['port_id']).data.decode('utf-8'))
                req['name'] = port['name'] + "/" + str(len(port['interfaces']) + 1)
            elif 'chan_id' in req:
                channel = json.loads(show_component(Channel, box_id, req['chan_id']).data.decode('utf-8'))
                req['name'] = channel['name'] + "/" + str(len(channel['interfaces']) + 1)
            elif 'logport_id' in req:
                logport = json.loads(show_component(LogPort, box_id, req['logport_id']).data.decode('utf-8'))
                req['name'] = logport['name'] + "/" + str(len(logport['interfaces']) + 1)
            else:
                raise exceptions.Forbidden('can not have port and channel as parent')
        elif box['vendor'] == 'EdgeCore':
            port = json.loads(show_component(Port, box_id, req['port_id']).data.decode('utf-8'))
            req['name'] = port['name']
    response = new_component(InterfaceSchema(), Interface, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/interfaces/<id>', methods=['PUT'])
def update_interface(box_id, id):
    req = flask.request.json
    update_component(Interface, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/interfaces/<id>', methods=['DELETE'])
def del_interface(box_id, id):
    del_component(Interface, box_id, id)
    return flask.Response(status=204)
