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
from ..models.cpeport_models import CpePort


class CpePortSchema(ma.Schema):
    class Meta:
        model = CpePort
        fields = ('id', 'box_id', 'box', 'cpe_id',
                  'name', 'description', 'cpe', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_cpe_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_cpe_ports', box_id='<box_id>')})


class CpePortsSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class CpePortSchema(ma.Schema):
        class Meta:
            model = CpePort
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_cpe_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(CpePortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_cpe_ports', box_id='<box_id>')})
