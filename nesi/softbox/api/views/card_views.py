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

from .base_views import *
from .box_views import show_box
from ..models.card_models import Card
from ..models.subrack_models import Subrack
from ..schemas.card_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/cards', methods=['GET'])
def show_cards(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(CardsSchema(), Card, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cards/<id>', methods=['GET'])
def show_card(box_id, id):
    response = show_component(Card, box_id, id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/cards', methods=['POST'])
def new_card(box_id):
    req = flask.request.json

    vendor = ''
    if 'name' not in req or req['name'] == "":
        subrack = json.loads(show_component(Subrack, box_id, req['subrack_id']).data.decode('utf-8'))
        box = json.loads(show_box(box_id)[0].data.decode('utf-8'))
        vendor = box['vendor']
        if len(subrack['cards']) > 0:
            last_card = subrack['cards'][len(subrack['cards']) - 1]
            if last_card['name'].startswith('nt-') and vendor == 'Alcatel':
                if subrack['name'] != "":
                    req['name'] = subrack['name'] + "/1"
                else:
                    req['name'] = "1"
            else:
                p = re.compile('^([0-9]+)?/?([0-9]+)?/?([0-9]+)?$')
                match_groups = p.match(last_card['name']).groups()
                filtered_match_groups = [x for x in match_groups if x is not None] # filter out None values
                last_card_index = filtered_match_groups[len(filtered_match_groups) - 1]
                if subrack['name'] != "":
                    req['name'] = subrack['name'] + "/" + str(int(last_card_index) + 1)
                else:
                    req['name'] = str(int(last_card_index) + 1)
        else:
            if subrack['name'] != "":
                if vendor == 'Huawei':
                    req['name'] = subrack['name'] + "/0"
                else:
                    req['name'] = subrack['name'] + "/1"
            else:
                if vendor == 'Huawei':
                    req['name'] = "0"
                else:
                    req['name'] = "1"

    if 'position' not in req or req['position'] == "" and vendor == 'Alcatel':
        req['position'] = 'lt:' + req['name']

    response = new_component(CardSchema(), Card, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/cards/<id>', methods=['PUT'])
def update_card(box_id, id):
    req = flask.request.json
    update_component(Card, req, box_id, id)
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/cards/<id>', methods=['DELETE'])
def del_card(box_id, id):
    del_component(Card, box_id, id)
    return flask.Response(status=204)
