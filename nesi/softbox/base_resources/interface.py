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

from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class Interface(base.Resource):
    """Represent logical interface resource."""

    id = base.Field('id')
    name = base.Field('name')
    description = base.Field('description')


class InterfaceCollection(base.ResourceCollection):
    """Represent a collection of interfaces."""

    @property
    def _resource_type(self):
        return Interface
