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

from sqlalchemy import func
#from nesi.softbox.api.models.box_models import Box
from experimental.interfaces.api_interface.views.config_views import app, flask, json, get_interface
from werkzeug import exceptions
from nesi.softbox.api import db



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
    INTERFACE = get_interface()
    box = INTERFACE.get_box(box_id)
    components = getattr(box, model)
    for component in components:
        if int(component.id) == int(id):
            break
    else:
        raise exceptions.NotFound(model + 'with id ' + id + ' not found')

    schema = component.Schema()
    response = schema.jsonify(component)
    INTERFACE.close_session()
    return response


def show_components(schema, model, req, box_id):
    INTERFACE = get_interface()
    box = INTERFACE.get_box(box_id)
    components = getattr(box, model)
    response = {
        'members': components,
        'count': len(components),
        'box_id': box_id
    }
    schemen = schema
    response = schemen.jsonify(response)
    INTERFACE.close_session()
    return response


def update_component(model, req, box_id, id):
    INTERFACE = get_interface()
    box = INTERFACE.get_box(box_id)
    components = getattr(box, model)
    for component in components:
        if int(component.id) == int(id):
            break
    else:
        raise exceptions.NotFound(model.__name__ + ' not found')

    for field in req:
        prev_attr = getattr(component, field)
        if isinstance(req[field], (type(None), type(prev_attr))) or isinstance(prev_attr, type(None)):
            setattr(component, field, req[field])
        else:
            raise exceptions.BadRequest('wrong datatype: ' + str(type(req[field])) + ' instead of ' + str(type(prev_attr)))

    INTERFACE.store(component)
    INTERFACE.close_session()


def del_component(model, box_id, id):
    INTERFACE = get_interface()
    box = INTERFACE.get_box(box_id)
    components = getattr(box, model)
    for component in components:
        if int(component.id) == int(id):
            break
    else:
        raise exceptions.NotFound(model.__name__ + ' not found')

    INTERFACE.delete(box_id, component)
    INTERFACE.close_session()


def get_vendor_specific_schema(component):
    '''box = (
        Box
        .query
        .filter_by(id=component.box_id)
        .first())

    try:
        schema = eval(box.vendor + type(component).__name__ + 'Schema')()

    except NameError:
        schema = eval(type(component).__name__ + 'Schema')()

    return schema'''


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
