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

import logging

from nesi.softbox import base

LOG = logging.getLogger(__name__)


class Subrack(base.Resource):
    """Represent physical shelf resource."""

    id = base.Field('id')
    name = base.Field('name')
    box_id = base.Field('box_id')
    description = base.Field('description')


class SubrackCollection(base.ResourceCollection):
    """Represent a collection of subracks."""

    @property
    def _resource_type(self):
        return Subrack
