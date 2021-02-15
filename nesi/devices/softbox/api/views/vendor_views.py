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
from ..schemas.vendor_schemas import *
from ..schemas.model_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/vendors', methods=['GET'])
def show_vendors():
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    vendors_query = (
        Vendor
        .query
        .filter_by(**req))

    vendors_query = search_model(Vendor, vendors_query)
    vendors = vendors_query.all()

    response = {}

    for vendor in vendors:
        models = {}
        for model in vendor.models:
            versions = []
            for version in model.versions:
                versions.append(version.name)
            models[model.name] = versions
        response[vendor.name] = models

    return flask.jsonify(response), 200


@app.route(PREFIX + '/vendors/<id>', methods=['GET'])
def show_vendor(id):
    vendor = (
        Vendor
        .query
        .filter_by(id=id)
        .first())

    if not vendor:
        raise exceptions.NotFound('Vendor not found')

    schema = VendorSchema()
    return schema.jsonify(vendor), 200


@app.route(PREFIX + '/vendors', methods=['POST'])
def new_vendor():
    req = flask.request.json
    vendor = Vendor(**req)

    db.session.add(vendor)
    db.session.commit()

    schema = VendorSchema()
    return schema.jsonify(vendor), 201


@app.route(PREFIX + '/vendors/<id>', methods=['DELETE'])
def del_vendor(id):
    vendor = (
        Vendor
        .query
        .filter_by(id=id)
        .first())

    if not vendor:
        raise exceptions.NotFound('Vendor not found')

    db.session.delete(vendor)
    db.session.commit()

    return flask.Response(status=204)


@app.route(PREFIX + '/vendors', methods=['DELETE'])
def cleanup_vendors():
    vendors_query = (
        Vendor
        .query
        .filter_by())

    vendors_query = search_model(Vendor, vendors_query)
    vendors = vendors_query.all()

    for vendor in vendors:
        for model in vendor.models:
            for version in model.versions:
                db.session.delete(version)
            db.session.delete(model)
        db.session.delete(vendor)

    db.session.commit()

    return flask.Response(status=204)
