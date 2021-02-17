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


class ServiceVlan(base.Resource):
    """Represent logical service vlan resource."""

    id = base.Field('id')
    name = base.Field('name')
    vlan_id = base.Field('vlan_id')
    service_port_id = base.Field('service_port_id')
    qos_profile_id = base.Field('qos_profile_id')
    scope = base.Field('scope')
    tag = base.Field('tag')
    card_id = base.Field('card_id')


class ServiceVlanCollection(base.ResourceCollection):
    """Represent a collection of logical service ports."""

    @property
    def _resource_type(self):
        return ServiceVlan
