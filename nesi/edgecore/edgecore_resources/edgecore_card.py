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

from nesi.softbox.base_resources.card import Card, CardCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class EdgeCoreCard(Card):
    """Represent physical shelf resource."""

    mac_address = base.Field('mac_address')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class EdgeCoreCardCollection(CardCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return EdgeCoreCard
