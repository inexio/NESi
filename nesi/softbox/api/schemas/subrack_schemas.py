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
from ..models.subrack_models import Subrack
from ..schemas.card_schemas import CardsSchema
from ..schemas.mgmt_card_schemas import MgmtCardsSchema


class SubrackSchema(ma.ModelSchema):
    class Meta:
        model = Subrack
        fields = ('id', 'box_id', 'box', 'cards', 'mgmt_cards',
                  'name', 'description', '_links')

    cards = ma.Nested(CardsSchema.CardSchema, many=True)
    mgmt_cards = ma.Nested(MgmtCardsSchema.MgmtCardSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_subrack', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor('show_subracks', box_id='<box_id>')})


class SubracksSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class SubrackSchema(ma.ModelSchema):
        class Meta:
            model = Subrack
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_subrack', box_id='<box_id>', id='<id>')})

    members = ma.Nested(SubrackSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_subracks', box_id='<box_id>')})
