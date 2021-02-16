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
from ..models.card_models import Card
from ..schemas.port_schemas import PortsSchema


class CardSchema(ma.Schema):
    class Meta:
        model = Card
        fields = ('id', 'box_id', 'box', 'subrack_id', 'ports', 'ppc',
                  'product', 'name', 'description', '_links')

    ports = ma.Nested(PortsSchema.PortSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_card', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor('show_cards', box_id='<box_id>')})


class CardsSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class CardSchema(ma.Schema):
        class Meta:
            model = Card
            fields = ('id', 'name', 'product', 'ppc', 'operational_state', 'ports', '_links')

        ports = ma.Nested(PortsSchema.PortSchema, many=True)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_card', box_id='<box_id>', id='<id>')})

    members = ma.Nested(CardSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_cards', box_id='<box_id>')})
