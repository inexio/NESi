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

from nesi.devices.softbox.base_resources.port import PortCollection, Port, logging, base

LOG = logging.getLogger(__name__)


class PBNPort(Port):
    """Represent physical port resource."""

    spanning_tree_guard_root = base.Field('spanning_tree_guard_root')
    switchport_trunk_vlan_allowed = base.Field('switchport_trunk_vlan_allowed')
    switchport_mode_trunk = base.Field('switchport_mode_trunk')
    switchport_pvid = base.Field('switchport_pvid')
    no_lldp_transmit = base.Field('no_lldp_transmit')
    pbn_speed = base.Field('pbn_speed')
    switchport_block_multicast = base.Field('switchport_block_multicast')
    switchport_rate_limit_egress = base.Field('switchport_rate_limit_egress')
    switchport_rate_limit_ingress = base.Field('switchport_rate_limit_ingress')
    no_pdp_enable = base.Field('no_pdp_enable')
    no_snmp_trap_link_status = base.Field('no_snmp_trap_link_status')
    exclamation_mark = base.Field('exclamation_mark')
    switchport_protected = base.Field('switchport_protected')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class PBNPortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return PBNPort
