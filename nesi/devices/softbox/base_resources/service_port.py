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

import logging

from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class ServicePort(base.Resource):
    """Represent logical service port resource."""

    id = base.Field('id')
    name = base.Field('name')
    connected_id = base.Field('connected_id')
    connected_type = base.Field('connected_type')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')

    def set_admin_state(self, status):
        """Set the admin-status of the service_port"""
        self.update(admin_state=status)

    def set_connected_id(self, id):
        """Set the port id to given id."""
        self.update(connected_id=id)

    def set_connected_type(self, obj):
        """Set is_configured_on to the given value"""
        self.update(connected_type=obj)


class ServicePortCollection(base.ResourceCollection):
    """Represent a collection of logical service ports."""

    @property
    def _resource_type(self):
        return ServicePort
