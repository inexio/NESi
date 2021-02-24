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


class QosInterface(base.Resource):
    """Represent a QosInterface resource."""

    id = base.Field('id')
    name = base.Field('name')
    description = base.Field('description')


class QosInterfaceCollection(base.ResourceCollection):
    """Represent the collection of QosInterfaces."""

    @property
    def _resource_type(self):
        return QosInterface
