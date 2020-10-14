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

# TODO: When no more new components are being created, update new_box, clone_box, and del_box

from .base_views import *
from ..models.box_models import Box
from ..models.credential_models import Credential
from ..models.subrack_models import Subrack
from ..models.card_models import Card
from ..models.port_models import Port
from ..models.cpe_models import Cpe
from ..models.cpeport_models import CpePort
from ..models.ont_models import Ont
from ..models.ontport_models import OntPort
from ..models.vlan_models import Vlan
from ..models.portprofile_models import PortProfile
from ..models.route_models import Route
from ..schemas.box_schemas import *

# KNAUP
import subprocess
import psutil
import os
import time

PREFIX = '/nesi/v1'


@app.route(PREFIX + '/')
def show_root():
    response = {
        'description': 'Network Equipment Simulator REST API ',
        'boxen': {
            '_links': {
                'self': flask.url_for('show_boxen')
            }
        }
    }

    schema = RootSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen', methods=['GET'])
def show_boxen():
    boxen_query = (
        Box
        .query)

    boxen_query = search_model(Box, boxen_query)

    boxen = boxen_query.all()
    response = {
        'members': boxen,
        'count': len(boxen)
    }

    schema = BoxenSchema()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<id>', methods=['GET'])
def show_box(id):
    box = (
        Box
        .query
        .filter_by(id=id)
        .first())

    if not box:
        raise exceptions.NotFound('Box not found')

    try:
        schema = eval(box.vendor + type(box).__name__ + 'Schema')()

    except NameError:
        schema = eval(type(box).__name__ + 'Schema')()
    return schema.jsonify(box), 200


@app.route(PREFIX + '/boxen', methods=['POST'])
def new_box():
    req = flask.request.json

    box_data = req.copy()

    # Additional components have to be wiped from box_data as a box can otherwise not be created
    components = ('credentials', 'subracks', 'cards', 'ports', 'onts', 'ont_ports', 'cpes', 'cpe_ports', 'vlans',
                  'port_profiles', 'routes')
    for component in components:
        if component in req:
            del box_data[component]

    box = Box(**box_data)
    db.session.add(box)
    db.session.flush()

    def create_subcomponent(components, component_model, reference_field=None, reference_mapping=None,
                            additional_reference_field=None, additional_reference_mapping=None):
        component_mapping = dict()
        for component in components:
            components[component]['box_id'] = box.id

            if reference_field and additional_reference_field:
                if reference_field in components[component]:
                    components[component][reference_field] = reference_mapping[components[component][reference_field]]
                elif additional_reference_field in components[component]:
                    components[component][additional_reference_field] = additional_reference_mapping[
                        components[component][additional_reference_field]]
            elif reference_field and (additional_reference_field is None):
                components[component][reference_field] = reference_mapping[components[component][reference_field]]

            component_obj = component_model(**components[component])
            db.session.add(component_obj)
            db.session.flush()

            component_mapping[int(component)] = component_obj.id

        return component_mapping

    create_subcomponent(req['credentials'], Credential) if 'credentials' in req else dict()
    subrack_mapping = create_subcomponent(req['subracks'], Subrack) if 'subracks' in req else dict()
    card_mapping = create_subcomponent(req['cards'], Card, 'subrack_id', subrack_mapping) if 'cards' in req else dict()
    port_mapping = create_subcomponent(req['ports'], Port, 'card_id', card_mapping) if 'ports' in req else dict()
    ont_mapping = create_subcomponent(req['onts'], Ont, 'port_id', port_mapping) if 'onts' in req else dict()
    ont_port_mapping = create_subcomponent(req['ont_ports'], OntPort, 'ont_id', ont_mapping) if 'ont_ports' in req else dict()
    cpe_mapping = create_subcomponent(req['cpes'], Cpe, 'port_id', port_mapping, 'ont_port_id', ont_port_mapping) if 'cpes' in req else dict()
    create_subcomponent(req['cpe_ports'], CpePort, 'cpe_id', cpe_mapping) if 'cpe_ports' in req else dict()
    create_subcomponent(req['vlans'], Vlan) if 'vlans' in req else dict()
    create_subcomponent(req['port_profiles'], PortProfile) if 'port_profiles' in req else dict()
    create_subcomponent(req['routes'], Route) if 'routes' in req else dict()

    db.session.commit()

    schema = BoxSchema()
    return schema.jsonify(box), 201


@app.route(PREFIX + '/boxen/<id>/clone', methods=['PUT'])
def clone_box(id):
    box = (
        Box
        .query
        .filter_by(id=id)
        .first())
    box_vars = vars(box).copy()

    del box_vars['_sa_instance_state']
    del box_vars['id']
    del box_vars['uuid']

    box_new = Box(**box_vars)
    db.session.add(box_new)
    db.session.flush()

    def clone_components(components, component_model, reference_field=None, reference_mapping=None,
                         additional_reference_field=None, additional_reference_mapping=None):
        component_mapping = dict()
        for component in components:
            component_vars = vars(component).copy()
            del component_vars['_sa_instance_state']
            del component_vars['id']
            component_vars['box_id'] = box_new.id
            if reference_field and additional_reference_field:
                if component_vars[reference_field]:
                    component_vars[reference_field] = reference_mapping[component_vars[reference_field]]
                elif component_vars[additional_reference_field]:
                    component_vars[additional_reference_field] = additional_reference_mapping[
                        component_vars[additional_reference_field]]
            elif reference_field and (additional_reference_field is None):
                component_vars[reference_field] = reference_mapping[component_vars[reference_field]]
            component_new = component_model(**component_vars)
            db.session.add(component_new)
            db.session.flush()
            component_mapping[component.id] = component_new.id
        return component_mapping

    _ = clone_components(box.credentials, Credential)
    subrack_mapping = clone_components(box.subracks, Subrack)
    card_mapping = clone_components(box.cards, Card, 'subrack_id', subrack_mapping)
    port_mapping = clone_components(box.ports, Port, 'card_id', card_mapping)
    ont_mapping = clone_components(box.onts, Ont, 'port_id', port_mapping)
    ont_port_mapping = clone_components(box.ont_ports, OntPort, 'ont_id', ont_mapping)
    cpe_mapping = clone_components(box.cpes, Cpe, 'port_id', port_mapping, 'ont_port_id', ont_port_mapping)
    clone_components(box.cpe_ports, CpePort, 'cpe_id', cpe_mapping)
    clone_components(box.vlans, Vlan)

    clone_components(box.port_profiles, PortProfile)
    clone_components(box.routes, Route)

    db.session.commit()

    schema = BoxSchema()
    return schema.jsonify(box_new), 201


@app.route(PREFIX + '/boxen/<id>', methods=['PUT'])
def update_box(id):
    req = flask.request.json

    box = (
        Box
        .query
        .filter_by(id=id)
        .first())

    for field in req:
        setattr(box, field, req[field])

    db.session.add(box)
    db.session.commit()
    return flask.Response(status=200)


@app.route(PREFIX + '/boxen/<id>', methods=['DELETE'])
def del_box(id):
    box = (
        Box
        .query
        .filter_by(id=id)
        .first())

    if not box:
        raise exceptions.NotFound('Box not found')

    def del_sub_components(component_collection):
        for component in component_collection:
            db.session.delete(component)

    del_sub_components(box.credentials)
    del_sub_components(box.subracks)
    del_sub_components(box.cards)
    del_sub_components(box.ports)
    del_sub_components(box.cpes)
    del_sub_components(box.cpe_ports)
    del_sub_components(box.onts)
    del_sub_components(box.ont_ports)
    del_sub_components(box.vlans)
    del_sub_components(box.port_profiles)
    del_sub_components(box.routes)
    del_sub_components(box.vlan_interfaces)
    del_sub_components(box.emus)
    del_sub_components(box.qos_interfaces)
    del_sub_components(box.users)

    db.session.delete(box)
    db.session.commit()

    return flask.Response(status=204)
