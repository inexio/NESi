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
from ..models.vlan_models import Vlan


class VlanSchema(ma.Schema):
    class Meta:
        model = Vlan
        fields = ('id', 'box_id', 'number', 'mtu', 'box', 'description', 'name',
                  '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks({
        'self': ma.URLFor(
            'show_vlan', box_id='<box_id>', id='<id>'),
        'collection': ma.URLFor(
            'show_vlans', box_id='<box_id>')})


class VlansSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class VlanSchema(ma.Schema):
        class Meta:
            model = Vlan
            fields = ('id', 'name', 'number', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_vlan', box_id='<box_id>', id='<id>')})

    members = ma.Nested(VlanSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor(
            'show_vlans', box_id='<box_id>')})
