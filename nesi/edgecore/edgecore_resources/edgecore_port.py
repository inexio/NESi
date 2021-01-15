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

from nesi.softbox.base_resources.port import Port, PortCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class EdgeCorePort(Port):
    """Represent physical port resource."""

    mac_address = base.Field('mac_address')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class EdgeCorePortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return EdgeCorePort
