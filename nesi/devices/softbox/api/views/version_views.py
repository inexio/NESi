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
from ..schemas.version_schemas import *
from ..schemas.version_schemas import *

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/versions', methods=['GET'])
def show_versions():
    if flask.request.args is None:
        req = {}
    else:
        req = flask.request.args

    versions_query = (
        Version
        .query
        .filter_by(**req))

    versions_query = search_model(Version, versions_query)
    versions = versions_query.all()

    response = {
        'members': versions,
        'count': len(versions)
    }

    schema = VersionsSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/versions/<id>', methods=['GET'])
def show_version(id):
    version = (
        Version
        .query
        .filter_by(id=id)
        .first())

    if not version:
        raise exceptions.NotFound('Version not found')

    schema = VersionSchema()
    return schema.jsonify(version), 200


@app.route(PREFIX + '/versions', methods=['POST'])
def new_version():
    req = flask.request.json
    version = Version(**req)

    db.session.add(version)
    db.session.commit()

    schema = VersionSchema()
    return schema.jsonify(version), 201


@app.route(PREFIX + '/versions/<id>', methods=['DELETE'])
def del_version(id):
    version = (
        Version
        .query
        .filter_by(id=id)
        .first())

    if not version:
        raise exceptions.NotFound('Version not found')

    db.session.delete(version)
    db.session.commit()

    return flask.Response(status=204)
