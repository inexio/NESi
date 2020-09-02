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

from nesi.softbox.base_resources.subrack import Subrack, SubrackCollection, logging, base

LOG = logging.getLogger(__name__)


class AlcatelSubrack(Subrack):
    """Represent physical shelf resource."""

    planned_type = base.Field('planned_type')
    actual_type = base.Field('actual_type')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')
    err_state = base.Field('err_state')
    availability = base.Field('availability')
    mode = base.Field('mode')
    subrack_class = base.Field('subrack_class')
    serial_no = base.Field('serial_no')
    variant = base.Field('variant')
    ics = base.Field('ics')


class AlcatelSubrackCollection(SubrackCollection):
    """Represent a collection of subracks."""

    @property
    def _resource_type(self):
        return AlcatelSubrack
