from nesi.devices.softbox.base_resources.service_port import ServicePort, ServicePortCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiServicePort(ServicePort):
    """Represent logical service port resource."""

    vpi = base.Field('vpi')
    vci = base.Field('vci')
    flow_type = base.Field('flow_type')
    flow_para = base.Field('flow_para')
    rx = base.Field('rx')
    tx = base.Field('tx')
    rx_cttr = base.Field('rx_cttr')
    tx_cttr = base.Field('tx_cttr')
    support_down_multicast_stream = base.Field('support_down_multicast_stream')
    support_igmp_packet = base.Field('support_igmp_packet')
    bytes_us = base.Field('bytes_us')
    packets_us = base.Field('packets_us')
    bytes_ds = base.Field('bytes_ds')
    packets_ds = base.Field('packets_ds')
    inbound_table_name = base.Field('inbound_table_name')
    outbound_table_name = base.Field('outbound_table_name')
    label = base.Field('label')
    priority = base.Field('priority')
    pvc_bundle = base.Field('pvc_bundle')
    max_mac_count = base.Field('max_mac_count')
    tag_transforms = base.Field('tag_transforms')
    description = base.Field('description')
    remote_description = base.Field('remote_description')
    service_port_bundle = base.Field('service_port_bundle')
    cos = base.Field('cos')
    static_mac = base.Field('static_mac')
    ip_address = base.Field('ip_address')

    def set_vpi(self, vpi):
        """Set the vpi to given value."""
        self.update(vpi=vpi)

    def set_vci(self, vci):
        """Set the vci to given value."""
        self.update(vci=vci)

    def set_inbound_table_name(self, inbound_table_name):
        """Set the inbound_table_name to given value."""
        self.update(inbound_table_name=inbound_table_name)

    def set_outbound_table_name(self, outbound_table_name):
        """Set the outbound_table_name to given value."""
        self.update(outbound_table_name=outbound_table_name)


class HuaweiServicePortCollection(ServicePortCollection):
    """Represent a collection of logical service ports."""

    @property
    def _resource_type(self):
        return HuaweiServicePort
