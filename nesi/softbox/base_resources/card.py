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

import logging

from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class Card(base.Resource):
    """Represent physical shelf resource."""
    id = base.Field('id')
    name = base.Field('name')
    box_id = base.Field('box_id')
    subrack_id = base.Field('subrack_id')
    product = base.Field('product')
    description = base.Field('description')


class CardCollection(base.ResourceCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return Card
