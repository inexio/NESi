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

from nesi.devices.softbox.base_resources.port_profile import PortProfile, PortProfileCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelPortProfile(PortProfile):
    """Represent a PortProfile resource."""

    up_policer = base.Field('up_policer')
    down_policer = base.Field('down_policer')
    committed_info_rate = base.Field('committed_info_rate')
    committed_burst_size = base.Field('committed_burst_size')
    logical_flow_type = base.Field('logical_flow_type')


class AlcatelPortProfileCollection(PortProfileCollection):
    """Represent the collection of PortProfiles."""

    @property
    def _resource_type(self):
        return AlcatelPortProfile
