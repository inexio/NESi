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

from nesi.devices.softbox.base_resources.vlan import Vlan, VlanCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class EdgeCoreVlan(Vlan):
    """Represent a VLAN resource."""

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class EdgeCoreVlanCollection(VlanCollection):
    """Represent the collection of VLANs."""

    @property
    def _resource_type(self):
        return EdgeCoreVlan
