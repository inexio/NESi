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
from ..schemas.subrack_schemas import *


PREFIX = '/nesi/v1'


@app.route(PREFIX + '/boxen/<box_id>/subracks', methods=['GET'])
def show_subracks(box_id):
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    response = show_components(SubracksSchema(), Subrack, req, box_id)
    return response, 200


@app.route(PREFIX + '/boxen/<box_id>/subracks/<id>', methods=['GET'])
def show_subrack(box_id, id):
    subrack = (
        Subrack
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not subrack:
        raise exceptions.NotFound('Subrack not found')

    schema = get_vendor_specific_schema(subrack)
    return schema.jsonify(subrack), 200


@app.route(PREFIX + '/boxen/<box_id>/subracks', methods=['POST'])
def new_subrack(box_id):
    req = flask.request.json
    response = new_component(SubrackSchema(), Subrack, req, box_id)
    return response, 201


@app.route(PREFIX + '/boxen/<box_id>/subracks/<id>', methods=['PUT'])
def update_subrack(box_id, id):
    subrack = (
        Subrack
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not subrack:
        raise exceptions.NotFound('Subrack not found')

    req = flask.request.json

    for field in req:
        setattr(subrack, field, req[field])

    db.session.add(subrack)
    db.session.commit()

    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<box_id>/subracks/<id>', methods=['DELETE'])
def del_subrack(box_id, id):
    subrack = (
        Subrack
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not subrack:
        raise exceptions.NotFound('Subrack not found')

    db.session.delete(subrack)
    db.session.commit()

    return flask.Response(status=204)
