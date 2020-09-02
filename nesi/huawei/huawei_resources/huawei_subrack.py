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

from nesi.softbox.base_resources.subrack import SubrackCollection, Subrack, logging, base

LOG = logging.getLogger(__name__)


class HuaweiSubrack(Subrack):
    """Represent physical shelf resource."""

    # huawei specific data fields
    frame_status = base.Field('frame_status')
    temperature = base.Field('temperature')


class HuaweiSubrackCollection(SubrackCollection):
    """Represent a collection of subracks."""

    @property
    def _resource_type(self):
        return HuaweiSubrack
