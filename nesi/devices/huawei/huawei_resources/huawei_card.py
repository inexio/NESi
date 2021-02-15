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

from nesi.devices.softbox.base_resources.card import Card, CardCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiCard(Card):
    """Represent physical shelf resource."""

    board_name = base.Field('board_name')
    board_status = base.Field('board_status')
    sub_type_0 = base.Field('sub_type_0')
    sub_type_1 = base.Field('sub_type_1')
    power_status = base.Field('power_status')
    power_off_cause = base.Field('power_off_cause')
    power_off_time = base.Field('power_off_time')
    temperature = base.Field('temperature')


class HuaweiCardCollection(CardCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return HuaweiCard
