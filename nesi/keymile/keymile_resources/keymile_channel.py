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


class KeyMileChannel(base.Resource):
    """Represent logical channel resource."""

    id = base.Field('id')
    port_id = base.Field('port_id')
    name = base.Field('name')
    description = base.Field('description')
    chan_profile_name = base.Field('chan_profile_name')
    curr_rate_u = base.Field('curr_rate_u')
    curr_rate_d = base.Field('curr_rate_d')
    prev_rate_u = base.Field('prev_rate_u')
    prev_rate_d = base.Field('prev_rate_d')
    curr_delay_u = base.Field('curr_delay_u')
    curr_delay_d = base.Field('curr_delay_d')

    def set_profile_name(self, name):
        self.update(chan_profile_name=name)


class KeyMileChannelCollection(base.ResourceCollection):
    """Represent a collection of channels."""

    @property
    def _resource_type(self):
        return KeyMileChannel
