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
