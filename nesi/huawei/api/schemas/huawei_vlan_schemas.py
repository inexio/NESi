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

from nesi.softbox.api.schemas.vlan_schemas import *


class HuaweiVlanSchema(VlanSchema):
    class Meta:
        model = Vlan
        fields = VlanSchema.Meta.fields + \
                 ('type', 'attribute', 'bind_service_profile_id', 
                  'bind_RAIO_profile_index', 'priority', 'state',
                  'native_vlan', 'sending_frames_format', 'hardware_address', 'vmac_ipoe', 'vmac_pppoe', 'vmac_pppoa',
                  'vlan_mac', 'packet_policy_multicast', 'packet_policy_unicast', 'security_anti_ipspoofing',
                  'security_anti_macspoofing', 'igmp_mismatch', 'tag')
