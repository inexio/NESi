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

from nesi.devices.softbox.base_resources.service_port import logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeyMileSrvc(base.Resource):
    """Represent logical srvc resource."""

    id = base.Field('id')
    name = base.Field('name')
    service_type = base.Field('service_type')
    address = base.Field('address')
    svid = base.Field('svid')
    stag_priority = base.Field('stag_priority')
    vlan_handling = base.Field('vlan_handling')

    def set_service(self, address, svid, stag_prio, vlan):
        self.update(address=address)
        self.update(svid=svid)
        self.update(stag_priority=stag_prio)
        self.update(vlan_handling=vlan)


class KeyMileSrvcCollection(base.ResourceCollection):
    """Represent a collection of logical srvcs."""

    @property
    def _resource_type(self):
        return KeyMileSrvc
