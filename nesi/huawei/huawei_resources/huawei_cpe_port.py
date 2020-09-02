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

from nesi.softbox.base_resources.cpe_port import CpePort, CpePortCollection, logging

LOG = logging.getLogger(__name__)


class HuaweiCpePort(CpePort):
    """Represent physical cpe port resource."""

    # huawei specific data fields


class HuaweiCpePortCollection(CpePortCollection):
    """Represent a collection of cpe ports."""

    @property
    def _resource_type(self):
        return HuaweiCpePort
