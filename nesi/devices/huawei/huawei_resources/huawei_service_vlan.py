from nesi.devices.softbox.base_resources.service_vlan import ServiceVlan, ServiceVlanCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiServiceVlan(ServiceVlan):
    """Represent logical service vlan resource."""

    tag = base.Field('tag')
    mode = base.Field('mode')

    def set_tag(self, tag):
        """Set the tag to given value."""
        self.update(tag=tag)

    def set_service_port_id(self, id):
        """Set the service port id to given id."""
        self.update(service_port_id=id)

    def set_mode(self, mode):
        """Set the mode to given vlaue."""
        self.update(mode=mode)


class HuaweiServiceVlanCollection(ServiceVlanCollection):
    """Represent a collection of logical service vlans."""

    @property
    def _resource_type(self):
        return HuaweiServiceVlan
