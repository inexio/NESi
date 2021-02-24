# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

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
