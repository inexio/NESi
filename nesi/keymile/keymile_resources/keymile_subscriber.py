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

from nesi.softbox.base_resources.service_port import logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeymileSubscriber(base.Resource):
    """Represent logical subscriber resource."""

    # fields
    id = base.Field('id')
    number = base.Field('number')
    name = base.Field('name')
    type = base.Field('type')
    address = base.Field('address')
    registration_state = base.Field('registration_state')


class KeymileSubscriberCollection(base.ResourceCollection):
    """Represent a collection of logical subscribers."""

    @property
    def _resource_type(self):
        return KeymileSubscriber
