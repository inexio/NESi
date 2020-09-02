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
from ..schemas.model_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/models', methods=['GET'])
def show_models():
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    models_query = (
        Model
        .query
        .filter_by(**req))

    models_query = search_model(Model, models_query)
    models = models_query.all()

    response = {
        'members': models,
        'count': len(models)
    }

    schema = ModelsSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/models/<id>', methods=['GET'])
def show_model(id):
    model = (
        Model
        .query
        .filter_by(id=id)
        .first())

    if not model:
        raise exceptions.NotFound('Model not found')

    schema = ModelSchema()
    return schema.jsonify(model), 200


@app.route(PREFIX + '/models', methods=['POST'])
def new_model():
    req = flask.request.json
    model = Model(**req)

    db.session.add(model)
    db.session.commit()

    schema = ModelSchema()
    return schema.jsonify(model), 201


@app.route(PREFIX + '/models/<id>', methods=['DELETE'])
def del_model(id):
    model = (
        Model
        .query
        .filter_by(id=id)
        .first())

    if not model:
        raise exceptions.NotFound('Model not found')

    db.session.delete(model)
    db.session.commit()

    return flask.Response(status=204)
