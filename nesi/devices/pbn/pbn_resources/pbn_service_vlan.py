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

from nesi.devices.softbox.base_resources.service_vlan import ServiceVlan, ServiceVlanCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class PBNServiceVlan(ServiceVlan):
    """Represent logical service vlan resource."""


class PBNServiceVlanCollection(ServiceVlanCollection):
    """Represent a collection of logical service vlans."""

    @property
    def _resource_type(self):
        return PBNServiceVlan
