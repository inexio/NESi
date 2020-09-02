from nesi.softbox.api.schemas.ontport_schemas import *


class HuaweiOntPortSchema(OntPortSchema):
    class Meta:
        model = OntPort
        fields = OntPortSchema.Meta.fields + ('ont_port_index', 'ont_port_type', 'speed', 'duplex',
                                              'link_state', 'ring_status', 'qinq_mode', 'priority_policy', 'inbound',
                                              'outbound', 'downstream_mode', 'mismatch_policy',
                                              'dscp_mapping_table_index', 'service_type', 'service_index', 's_vlan',
                                              's_pri', 'c_vlan', 'c_pri', 'encap', 's_pri_policy', 'igmp_mode',
                                              'igmp_vlan', 'igmp_pri', 'max_mac_count', 'vlan_id', 'operational_state')
