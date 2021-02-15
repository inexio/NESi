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

from nesi.devices.softbox.api import ma
from ..models.ont_models import Ont
from ..schemas.ontport_schemas import OntPortsSchema


class OntSchema(ma.ModelSchema):
    class Meta:
        model = Ont
        fields = ('id', 'box_id', 'box', 'port_id', 'ont_ports',
                  'name', 'description', '_links', 'admin_state', 'operational_state')

    ont_ports = ma.Nested(OntPortsSchema.OntPortSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_ont', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_onts', box_id='<box_id>')})


class OntsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class OntSchema(ma.ModelSchema):
        class Meta:
            model = Ont
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_ont', box_id='<box_id>', id='<id>')})

    members = ma.Nested(OntSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_onts', box_id='<box_id>')})
