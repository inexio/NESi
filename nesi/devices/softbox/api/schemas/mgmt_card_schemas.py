# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.devices.softbox.api import ma
from ..models.mgmt_card_models import MgmtCard
from ..schemas.mgmt_port_schemas import MgmtPortsSchema


class MgmtCardSchema(ma.Schema):
    class Meta:
        model = MgmtCard
        fields = ('id', 'box_id', 'box', 'name', 'subrack_id', 'admin_state', 'operational_state', 'description',
                  'mgmt_ports')

    mgmt_ports = ma.Nested(MgmtPortsSchema.MgmtPortSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_mgmt_card', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor('show_mgmt_cards', box_id='<box_id>')})


class MgmtCardsSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class MgmtCardSchema(ma.Schema):
        class Meta:
            model = MgmtCard
            fields = ('id', 'name', 'operational_state', 'mgmt_ports', '_links')

        mgmt_ports = ma.Nested(MgmtPortsSchema.MgmtPortSchema, many=True)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_mgmt_card', box_id='<box_id>', id='<id>')})

    members = ma.Nested(MgmtCardSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_mgmt_cards', box_id='<box_id>')})
