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

from nesi.devices.softbox.api.schemas.service_port_schemas import *


class HuaweiServicePortSchema(ServicePortSchema):
    class Meta:
        model = ServicePort
        fields = ServicePortSchema.Meta.fields + ('vpi', 'vci', 'flow_type', 'tx_cttr', 'rx_cttr',
                                                  'flow_para', 'tx', 'inbound_table_name', 'rx', 'outbound_table_name',
                                                  'label', 'priority', 'support_down_multicast_stream',
                                                  'support_igmp_packet', 'bytes_us', 'packets_us', 'bytes_ds',
                                                  'packets_ds',
                                                  'pvc_bundle', 'max_mac_count', 'tag_transforms', 'description',
                                                  'remote_description', 'service_port_bundle', 'cos', 'static_mac',
                                                  'ip_address')
