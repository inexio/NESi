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

from nesi.devices.softbox.base_resources.ont import Ont, OntCollection, base
import logging

LOG = logging.getLogger(__name__)


class PBNOnt(Ont):
    """Represent physical shelf resource."""

    mac_address = base.Field('mac_address')


class PBNOntCollection(OntCollection):
    """Represent a collection of subracks."""

    @property
    def _resource_type(self):
        return PBNOnt
