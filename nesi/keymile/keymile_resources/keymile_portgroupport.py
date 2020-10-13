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

from nesi.softbox.base_resources.service_port import logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeymilePortGroupPort(base.Resource):
    """Represent logical subscriber resource."""

    # fields
    id = base.Field('id')
    name = base.Field('name')
    operational_state = base.Field('operational_state')
    admin_state = base.Field('admin_state')
    description = base.Field('description')
    label1 = base.Field('label1')
    label2 = base.Field('label2')

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)

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


class KeymilePortGroupPortCollection(base.ResourceCollection):
    """Represent a collection of logical subscribers."""

    @property
    def _resource_type(self):
        return KeymilePortGroupPort
