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
from ..models.ontport_models import OntPort
from ..schemas.cpe_schemas import CpesSchema


class OntPortSchema(ma.ModelSchema):
    class Meta:
        model = OntPort
        fields = ('id', 'box_id', 'box', 'ont_id', 'cpes',
                  'name', 'description', '_links', 'admin_state')

    cpes = ma.Nested(CpesSchema.CpeSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_ont_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_ont_ports', box_id='<box_id>')})


class OntPortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class OntPortSchema(ma.ModelSchema):
        class Meta:
            model = OntPort
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_ont_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(OntPortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_ont_ports', box_id='<box_id>')})
