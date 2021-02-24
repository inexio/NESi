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
from ..models.vlan_interface_models import VlanInterface


class VlanInterfaceSchema(ma.Schema):
    class Meta:
        model = VlanInterface
        fields = ('id', 'name', 'box', 'box_id', 'vlan_id', '_links')

        _links = ma.Hyperlinks({
            'self': ma.URLFor(
                'show_vlan_interface', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor(
                'show_vlan_interfaces', box_id='<box_id>')})


class VlanInterfacesSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class VlanInterfaceSchema(ma.Schema):
        class Meta:
            model = VlanInterface
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_vlan_interface', box_id='<box_id>', id='<id>')})

    members = ma.Nested(VlanInterfaceSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor(
            'show_vlan_interfaces', box_id='<box_id>')})
