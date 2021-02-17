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

import flask
import json
from sqlalchemy import func
from werkzeug import exceptions
from nesi.devices.softbox.api import app
from nesi.devices.softbox.api.models.box_models import Box
from nesi.devices.softbox.api.schemas import *
from nesi.devices.alcatel.api.schemas import *
from nesi.devices.huawei.api.schemas import *
from nesi.devices.keymile.api.schemas import *
from nesi.devices.edgecore.api.schemas import *
from nesi.devices.zhone.api.schemas import *
# important for other view classes
from nesi.devices.softbox.api import db

PREFIX = '/nesi/v1'


@app.errorhandler(exceptions.HTTPException)
def flask_exception_handler(exc):
    app.logger.error(exc)
    err = {
        'status': exc.code,
        'message': exc.description
    }
    response = flask.jsonify(err)
    response.status_code = exc.code
    return response


@app.errorhandler(Exception)
def all_exception_handler(exc):
    app.logger.error(exc)
    err = {
        'status': 400,
        'message': getattr(exc, 'message', str(exc))
    }
    response = flask.jsonify(err)
    response.status_code = 400
    return response


def new_component(schema, model, req, box_id):
    if isinstance(req, list):
        objs = ()
        for data in req:
            component = model(box_id=box_id, **data)
            db.session.add(component)
            db.session.flush()
            objs = (*objs, json.loads(schema.jsonify(component).response[0].decode('utf-8')))
        response = flask.jsonify(components=objs)
    else:
        component = model(box_id=box_id, **req)
        db.session.add(component)
        db.session.flush()
        response = schema.jsonify(component)

    db.session.commit()

    return response


def show_component(model, box_id, id):
    component = (
        model
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not component:
        raise exceptions.NotFound(model.__name__ + ' not found')

    schema = get_vendor_specific_schema(component)
    return schema.jsonify(component)


def show_components(schema, model, req, box_id):
    components_query = (
        model
        .query
        .filter_by(box_id=box_id, **req))

    components_query = search_model(model, components_query)

    components = components_query.all()
    response = {
        'members': components,
        'count': len(components),
        'box_id': box_id
    }

    return schema.jsonify(response)


def update_component(model, req, box_id, id):
    component = (
        model
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not component:
        raise exceptions.NotFound(str(model) + ' not found')

    for field in req:
        prev_attr = getattr(component, field)
        if isinstance(req[field], (type(None), type(prev_attr))) or isinstance(prev_attr, type(None)):
            setattr(component, field, req[field])
        else:
            raise exceptions.BadRequest('wrong datatype: ' + str(type(req[field])) + ' instead of ' + str(type(prev_attr)))

    db.session.add(component)
    db.session.commit()


def del_component(model, box_id, id):
    component = (
        model
        .query
        .filter_by(box_id=box_id, id=id)
        .first())

    if not component:
        raise exceptions.NotFound(str(model) + ' not found')

    db.session.delete(component)
    db.session.commit()


def get_vendor_specific_schema(component):
    box = (
        Box
        .query
        .filter_by(id=component.box_id)
        .first())

    try:
        schema = eval(box.vendor + type(component).__name__ + 'Schema')()

    except NameError:
        schema = eval(type(component).__name__ + 'Schema')()

    return schema


def search_model(model, query):

    known_columns = model.__table__.columns.keys()

    for search_column in flask.request.args:
        if search_column not in known_columns:
            raise exceptions.NotFound(
                'Search term %s is not supported' % search_column)

        search_terms = flask.request.args.getlist(search_column)
        if search_terms:
            search_terms = [term.lower() for term in search_terms]
            query = query.filter(
                func.lower(getattr(model, search_column)).in_(search_terms))

    return query
