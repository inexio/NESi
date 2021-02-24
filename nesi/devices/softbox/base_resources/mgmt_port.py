
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

import logging

from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class MgmtPort(base.Resource):
    """Represent physical port resource."""

    id = base.Field('id')
    name = base.Field('name')
    box_id = base.Field('box_id')
    card_id = base.Field('card_id')
    description = base.Field('description')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')

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
        """Set the port state to up"""
        self.update(operational_state='1')


class MgmtPortCollection(base.ResourceCollection):
    """Represent a collection of management ports."""

    @property
    def _resource_type(self):
        return MgmtPort
