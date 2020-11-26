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

from nesi.softbox.base_resources.interface import Interface, InterfaceCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class EdgeCoreInterface(Interface):
    """Represent a VlanInterface resource."""

    port_id = base.Field('port_id')
    ingress_state = base.Field('ingress_state')
    ingress_rate = base.Field('ingress_rate')
    egress_state = base.Field('egress_state')
    egress_rate = base.Field('egress_rate')
    vlan_membership_mode = base.Field('vlan_membership_mode')
    native_vlan = base.Field('native_vlan')
    allowed_vlan = base.Field('allowed_vlan')
    mac_address = base.Field('mac_address')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class EdgeCoreInterfaceCollection(InterfaceCollection):
    """Represent the collection of VlanInterfaces."""

    @property
    def _resource_type(self):
        return EdgeCoreInterface
