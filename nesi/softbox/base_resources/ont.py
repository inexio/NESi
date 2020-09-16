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

from nesi.softbox import base


class Ont(base.Resource):
    """Represent physical shelf resource."""

    id = base.Field('id')
    box_id = base.Field('box_id')
    port_id = base.Field('port_id')
    name = base.Field('name')
    description = base.Field('description')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')

    def down(self):
        """Change ont port admin state to down."""
        self.update(admin_state='0')

    def up(self):
        """Change ont port admin state to up."""
        self.update(admin_state='1')


class OntCollection(base.ResourceCollection):
    """Represent a collection of ONTs."""

    @property
    def _resource_type(self):
        return Ont
