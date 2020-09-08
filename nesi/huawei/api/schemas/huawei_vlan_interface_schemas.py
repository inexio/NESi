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

from nesi.softbox.api.schemas.vlan_interface_schemas import *


class HuaweiVlanInterfaceSchema(VlanInterfaceSchema):
    class Meta:
        model = VlanInterface
        fields = VlanInterfaceSchema.Meta.fields + ('admin_state', 'line_proto_state', 'input_packets', 'input_bytes',
                                                    'input_multicasts', 'output_packets', 'output_bytes',
                                                    'output_multicasts', 'internet_protocol', 'internet_address',
                                                    'subnet_num', 'broadcast_address', 'sending_frames_format',
                                                    'hardware_address', 'mtu')
