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

from nesi.devices.softbox.base_resources.service_port import logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeyMileLogPort(base.Resource):
    """Represent logical log_port resource."""

    id = base.Field('id')
    name = base.Field('name')
    card_id = base.Field('card_id')
    ports = base.Field('ports')
    label1 = base.Field('label1')
    label2 = base.Field('label2')
    description = base.Field('description')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')
    profile = base.Field('profile')

    def admin_up(self):
        """Set the admin port state to up"""
        self.update(admin_state='1')

    def admin_down(self):
        """Set the admin port state to down"""
        self.update(admin_state='0')

    def down(self):
        """Set the port state to down"""
        self.update(operational_state='0')

    def up(self):
        """Set the port state to down"""
        self.update(operational_state='1')

    def set_profile(self, profile):
        self.update(profile=profile)

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)


class KeyMileLogPortCollection(base.ResourceCollection):
    """Represent a collection of logical log_ports."""

    @property
    def _resource_type(self):
        return KeyMileLogPort
