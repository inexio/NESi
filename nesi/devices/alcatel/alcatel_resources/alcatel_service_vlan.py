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

from nesi.devices.softbox.base_resources.service_vlan import ServiceVlan, ServiceVlanCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelServiceVlan(ServiceVlan):
    """Represent logical service vlan resource."""

    l2fwder_vlan = base.Field('l2fwder_vlan')
    scope = base.Field('scope')
    tag = base.Field('tag')

    def set_l2fwder_vlan(self, vlan_number):
        """Set the set_l2fwder_vlan to given vlan-number."""
        self.update(l2fwder_vlan=vlan_number)

    def set_scope(self, scope):
        """Set the scope to given value."""
        self.update(scope=scope)

    def set_tag(self, tag):
        """Set the tag to given value."""
        self.update(tag=tag)


class AlcatelServiceVlanCollection(ServiceVlanCollection):
    """Represent a collection of logical service vlans."""

    @property
    def _resource_type(self):
        return AlcatelServiceVlan
