from nesi.softbox.api.schemas.vlan_interface_schemas import *


class HuaweiVlanInterfaceSchema(VlanInterfaceSchema):
    class Meta:
        model = VlanInterface
        fields = VlanInterfaceSchema.Meta.fields + ('admin_state', 'line_proto_state', 'input_packets', 'input_bytes',
                                                    'input_multicasts', 'output_packets', 'output_bytes',
                                                    'output_multicasts', 'internet_protocol', 'internet_address',
                                                    'subnet_num', 'broadcast_address')
