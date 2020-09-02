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

from nesi.softbox.base_resources.port_profile import PortProfile, PortProfileCollection, logging

LOG = logging.getLogger(__name__)


class HuaweiPortProfile(PortProfile):
    """Represent a PortProfile resource."""

    # huawei specific data fields


class HuaweiPortProfileCollection(PortProfileCollection):
    """Represent the collection of PortProfiles."""

    @property
    def _resource_type(self):
        return HuaweiPortProfile
