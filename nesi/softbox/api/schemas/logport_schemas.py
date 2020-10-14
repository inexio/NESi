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

from nesi.softbox.api import ma
from .interface_schemas import InterfacesSchema
from ..models.logport_models import LogPort


class LogPortSchema(ma.ModelSchema):
    class Meta:
        model = LogPort
        fields = ('id', 'box_id', 'box', 'card_id', 'name', 'ports', 'interfaces', 'description', 'admin_state',
                  'operational_state', 'label1', 'label2',
                  '_links')

    interfaces = ma.Nested(InterfacesSchema.InterfaceSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_logport', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_logports', box_id='<box_id>')})


class LogPortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class LogPortSchema(ma.ModelSchema):
        class Meta:
            model = LogPort
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_logport', box_id='<box_id>', id='<id>')})

    members = ma.Nested(LogPortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_logports', box_id='<box_id>')})
