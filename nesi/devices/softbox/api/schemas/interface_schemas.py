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
from ..models.interface_models import Interface


class InterfaceSchema(ma.ModelSchema):
    class Meta:
        model = Interface
        fields = ('id', 'box_id', 'box', 'name', 'description', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_interface', box_id='<box_id>', id='<id>')})


class InterfacesSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class InterfaceSchema(ma.ModelSchema):
        class Meta:
            model = Interface
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_interface', box_id='<box_id>', id='<id>')})

    members = ma.Nested(InterfaceSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_interfaces', box_id='<box_id>')})


