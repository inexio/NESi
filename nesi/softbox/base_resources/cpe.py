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

from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class Cpe(base.Resource):
    """Represent physical cpe resource."""

    id = base.Field('id')
    port_id = base.Field('port_id')
    ont_port_id = base.Field('ont_port_id')
    name = base.Field('name')
    description = base.Field('description')
    serial_no = base.Field('serial_no')
    admin_state = base.Field('admin_state')
    mac = base.Field('mac')

    def down(self):
        """Change ont port admin state to down."""
        self.update(admin_state='0')

    def up(self):
        """Change ont port admin state to up."""
        self.update(admin_state='1')


class CpeCollection(base.ResourceCollection):
    """Represent a collection of cpes."""

    @property
    def _resource_type(self):
        return Cpe
