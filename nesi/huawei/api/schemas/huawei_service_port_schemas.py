from nesi.softbox.api.schemas.service_port_schemas import *


class HuaweiServicePortSchema(ServicePortSchema):
    class Meta:
        model = ServicePort
        fields = ServicePortSchema.Meta.fields + ('vpi', 'vci', 'flow_type',
                                                  'flow_para', 'tx', 'inbound_table_name', 'rx', 'outbound_table_name',
                                                  'label', 'priority', 'support_down_multicast_stream',
                                                  'support_igmp_packet', 'bytes_us', 'packets_us', 'bytes_ds',
                                                  'packets_ds',
                                                  'pvc_bundle', 'max_mac_count', 'tag_transforms', 'description',
                                                  'remote_description', 'service_port_bundle', 'cos', 'static_mac',
                                                  'ip_address')
