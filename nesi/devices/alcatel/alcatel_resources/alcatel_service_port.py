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

from nesi.devices.softbox.base_resources.service_port import ServicePort, ServicePortCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelServicePort(ServicePort):
    """Represent logical service port resource."""

    pvid = base.Field('pvid')
    qos_profile_id = base.Field('qos_profile_id')
    max_unicast_mac = base.Field('max_unicast_mac')
    pvc = base.Field('pvc')

    def set_max_unicast_mac(self, value):
        """Set the max_unicast_mac value"""
        self.update(max_unicast_mac=value)

    def set_qos_profile(self, profile_id):
        """Set the qos_profile_id to given id."""
        self.update(qos_profile_id=profile_id)

    def set_pvid(self, value):
        """Set the pvid value to given val"""
        self.update(pvid=value)


class AlcatelServicePortCollection(ServicePortCollection):
    """Represent a collection of logical service ports."""

    @property
    def _resource_type(self):
        return AlcatelServicePort
