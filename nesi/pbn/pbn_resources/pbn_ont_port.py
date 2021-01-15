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

from nesi.softbox.base_resources.ont_port import OntPort, OntPortCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class PBNOntPort(OntPort):
    """Represent physical ONT port resource."""
    operational_state = base.Field('operational_state')
    admin_state = base.Field('admin_state')
    flow_control = base.Field('flow_control')
    duplex = base.Field('duplex')
    speed = base.Field('speed')
    storm_control = base.Field('storm_control')


class PBNOntPortCollection(OntPortCollection):
    """Represent a collection of ONT ports."""

    @property
    def _resource_type(self):
        return PBNOntPort
