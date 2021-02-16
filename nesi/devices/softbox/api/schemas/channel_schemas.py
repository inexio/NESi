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
from ..models.channel_models import Channel
from ..schemas.interface_schemas import InterfacesSchema


class ChannelSchema(ma.Schema):
    class Meta:
        model = Channel
        fields = ('id', 'box_id', 'box', 'port_id', 'interfaces', 'curr_rate_u', 'curr_rate_d', 'prev_rate_u',
                  'name', 'description', 'prev_rate_d', 'curr_delay_u', 'curr_delay_d', '_links')

    interfaces = ma.Nested(InterfacesSchema.InterfaceSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_channel', box_id='<box_id>', id='<id>')})


class ChannelsSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class ChannelSchema(ma.Schema):
        class Meta:
            model = Channel
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_channel', box_id='<box_id>', id='<id>')})

    members = ma.Nested(ChannelSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_channels', box_id='<box_id>')})


