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
from ..schemas.subscriber_schemas import *
from ..models.portgroupport_models import PortGroupPort

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/subscribers', methods=['GET'])
def show_subscribers(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(SubscribersSchema(), Subscriber, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/subscribers/<id>', methods=['GET'])
def show_subscriber(box_id, id):
    response = show_component(Subscriber, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/subscribers/<id>', methods=['PUT'])
def update_subscriber(box_id, id):
    req = flask.request.json
    update_component(Subscriber, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/subscribers', methods=['POST'])
def new_subscriber(box_id):
    req = flask.request.json
    portgroupport = json.loads(show_component(PortGroupPort, box_id, req['portgroupport_id']).data.decode('utf-8'))
    req['address'] = '/portgroup-' + portgroupport['name'].split('/')[1][1:] + '/port-' + portgroupport['name'].split('/')[2]
    response = new_component(SubscriberSchema(), Subscriber, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/subscribers/<id>', methods=['DELETE'])
def del_subscriber(box_id, id):
    del_component(Subscriber, box_id, id)
    return flask.Response(status=204)
