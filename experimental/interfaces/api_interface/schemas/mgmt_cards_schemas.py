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

from nesi.softbox.api import ma
from experimental.db_models.alcatel.mgmt_card_models import AlcatelMgmtCard


class MgmtCardsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class MgmtCardSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelMgmtCard
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_mgmt_card', box_id='<box_id>', id='<id>')})

    members = ma.Nested(MgmtCardSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_mgmt_cards', box_id='<box_id>')})
