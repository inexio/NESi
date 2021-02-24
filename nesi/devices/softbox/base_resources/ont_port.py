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


class OntPort(base.Resource):
    """Represent physical ONT port resource."""

    id = base.Field('id')
    box_id = base.Field('box_id')
    ont_id = base.Field('ont_id')
    name = base.Field('name')
    description = base.Field('description')


class OntPortCollection(base.ResourceCollection):
    """Represent a collection of ONT ports."""

    @property
    def _resource_type(self):
        return OntPort
