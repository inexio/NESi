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

from nesi.softbox.base_resources.ont_port import OntPortCollection, OntPort, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelOntPort(OntPort):
    """Represent physical ONT port resource."""

    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')
    uni_idx = base.Field('uni_idx')
    config_indicator = base.Field('config_indicator')
    link_status = base.Field('link_status')
    speed = base.Field('speed')

    def port_up(self):
        """Change ont port state to up."""
        self.update(operational_state='1')

    def port_down(self):
        """Change ont port state to down."""
        self.update(operational_state='0')

    def admin_up(self):
        """Change ont port admin state to up."""
        self.update(admin_state='1')

    def admin_down(self):
        """Change ont port admin state to down."""
        self.update(admin_state='0')

    def set_description(self, user):
        """Set the description of the ont port"""
        self.update(description=user)

    def set_speed(self, speed):
        """Set the speed of the ont port"""
        self.update(speed=speed)


class AlcatelOntPortCollection(OntPortCollection):
    """Represent a collection of ONT ports."""

    @property
    def _resource_type(self):
        return AlcatelOntPort
