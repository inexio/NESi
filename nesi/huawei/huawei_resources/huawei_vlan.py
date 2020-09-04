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

from nesi.softbox.base_resources.vlan import Vlan, VlanCollection, base, logging

LOG = logging.getLogger(__name__)


class HuaweiVlan(Vlan):
    """Represent a VLAN resource."""

    type = base.Field('type')
    attribute = base.Field('attribute')
    bind_service_profile_id = base.Field('bind_service_profile_id')
    bind_RAIO_profile_index = base.Field('bind_RAIO_profile_index')
    priority = base.Field('priority')
    state = base.Field('state')
    native_vlan = base.Field('native_vlan')
    sending_frames_format = base.Field('sending_frames_format')
    hardware_address = base.Field('hardware_address')
    vmac_ipoe = base.Field('vmac_ipoe')
    vmac_pppoe = base.Field('vmac_pppoe')
    vmac_pppoa = base.Field('vmac_pppoa')
    vlan_mac = base.Field('vlan_mac')
    packet_policy_multicast = base.Field('packet_policy_multicast')
    packet_policy_unicast = base.Field('packet_policy_unicast')
    security_anti_ipspoofing = base.Field('security_anti_ipspoofing')
    security_anti_macspoofing = base.Field('security_anti_macspoofing')
    igmp_mismatch = base.Field('igmp_mismatch')
    tag = base.Field('tag')

    def set_tag(self, tag):
        """Set the tag to given value."""
        self.update(tag=tag)

    def set_type_smart(self):
        """Change the type to smart"""
        self.update(type="smart")

    def set_service_profile_id(self, id):
        """Set service profile_id"""
        self.update(bind_service_profile_id=id)


class HuaweiVlanCollection(VlanCollection):
    """Represent the collection of VLANs."""

    @property
    def _resource_type(self):
        return HuaweiVlan
