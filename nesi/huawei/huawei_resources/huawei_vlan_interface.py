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

from nesi.softbox.base_resources.vlan_interface import VlanInterface, VlanInterfaceCollection, logging, base

LOG = logging.getLogger(__name__)


class HuaweiVlanInterface(VlanInterface):
    """Represent a VlanInterface resource."""

    admin_state = base.Field('admin_state')
    line_proto_state = base.Field('line_proto_state')
    input_packets = base.Field('input_packets')
    input_bytes = base.Field('input_bytes')
    input_multicasts = base.Field('input_multicasts')
    output_packets = base.Field('output_packets')
    output_bytes = base.Field('output_bytes')
    output_multicasts = base.Field('output_multicasts')
    internet_protocol = base.Field('internet_protocol')
    internet_address = base.Field('internet_address')
    subnet_num = base.Field('subnet_num')
    broadcast_address = base.Field('broadcast_address')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class HuaweiVlanInterfaceCollection(VlanInterfaceCollection):
    """Represent the collection of VlanInterfaces."""

    @property
    def _resource_type(self):
        return HuaweiVlanInterface
