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

import re
from .box_views import show_box
from experimental.interfaces.api_interface.views.config_views import app, PREFIX, flask
from experimental.interfaces.api_interface.schemas.mgmt_cards_schemas import MgmtCardsSchema
from experimental.interfaces.api_interface.views.base_views import *


@app.route(PREFIX + '/boxen/<box_id>/mgmt_cards', methods=['GET'])
def show_mgmt_cards(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(MgmtCardsSchema(), 'mgmt_cards', req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/mgmt_cards/<id>', methods=['GET'])
def show_mgmt_card(box_id, id):
    response = show_component('mgmt_cards', box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/mgmt_cards', methods=['POST'])
def new_mgmt_card(box_id):
    req = flask.request.json

    '''box = json.loads(show_box(box_id)[0].data.decode('utf-8'))
    subrack = json.loads(show_component(Subrack, box_id, req['subrack_id']).data.decode('utf-8'))
    if 'name' not in req or req['name'] == '' or req['name'] not in ('11', '13'):
        if box['vendor'] == 'KeyMile':
            card11_exists = False
            card13_exists = False
            for card in subrack['mgmt_cards']:
                if card['name'] == '11':
                    card11_exists = True
                elif card['name'] == '13':
                    card13_exists = True
            if not card11_exists:
                req['name'] = '11'
            elif not card13_exists:
                req['name'] = '13'
            else:
                return flask.Response(status=500)

    response = new_component(MgmtCardSchema(), MgmtCard, req, box_id)
    return response, 201'''


@app.route(PREFIX + '/boxen/<box_id>/mgmt_cards/<id>', methods=['PUT'])
def update_mgmt_card(box_id, id):
    req = flask.request.json
    update_component('mgmt_cards', req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/mgmt_cards/<id>', methods=['DELETE'])
def del_mgmt_card(box_id, id):
    del_component('mgmt_cards', box_id, id)
    return flask.Response(status=204)
