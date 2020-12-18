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
from ..models.port_models import Port
from ..schemas.cpe_schemas import CpesSchema
from ..schemas.ont_schemas import OntsSchema
from ..schemas.channel_schemas import ChannelsSchema
from ..schemas.interface_schemas import InterfacesSchema


class PortSchema(ma.ModelSchema):
    class Meta:
        model = Port
        fields = ('id', 'box_id', 'box', 'card_id', 'cpes', 'onts', 'channels', 'loopback', 'name', 'interfaces',
                  'description', 'admin_state', 'operational_state', '_links')

    cpes = ma.Nested(CpesSchema.CpeSchema, many=True)

    onts = ma.Nested(OntsSchema.OntSchema, many=True)

    channels = ma.Nested(ChannelsSchema.ChannelSchema, many=True)

    interfaces = ma.Nested(InterfacesSchema.InterfaceSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_ports', box_id='<box_id>')})


class PortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class PortSchema(ma.ModelSchema):
        class Meta:
            model = Port
            fields = ('id', 'name', 'operational_state', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(PortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_ports', box_id='<box_id>')})
