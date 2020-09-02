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

from nesi.alcatel.alcatel_resources.alcatel_box import *
from nesi.huawei.huawei_resources.huawei_box import *
from nesi.edgecore.edgecore_resources.edgecore_box import *
from nesi.keymile.keymile_resources.keymile_box import *
from nesi.pbn.pbn_resources.pbn_box import *
from nesi.zhone.zhone_resources.zhone_box import *

LOG = logging.getLogger(__name__)


class Root(base.Resource):
    """NESi REST API service root.

    :param connector: A RestClient instance
    :param path: sub-URI path to the resource.
    """

    description = base.Field('description')
    """Service description."""

    def __init__(self, connector, path='/nesi/v1'):

        super(Root, self).__init__(connector, path=path)

    def boxen(self):
        """Return a `BoxCollection` object."""
        return BoxCollection(self._conn, base.get_sub_resource_path_by(self, 'boxen'))

    def get_box(self, identity, vendor=None):
        """Return `Box` object by identity.

        :param identity: The identity of the Box resource.
        :raises: `UnknownDefaultError` if default box can't be determined.
        :returns: The Box object
        """
        if vendor is None:
            return Box(self._conn, identity)
        elif vendor == "Alcatel":
            return AlcatelBox(self._conn, identity)
        elif vendor == "Huawei":
            return HuaweiBox(self._conn, identity)
        elif vendor == "EdgeCore":
            return EdgeCoreBox(self._conn, identity)
        elif vendor == "KeyMile":
            return KeyMileBox(self._conn, identity)
        elif vendor == "PBN":
            return PBNBox(self._conn, identity)
        elif vendor == "Zhone":
            return ZhoneBox(self._conn, identity)
        else:
            raise Exception("wrong box vendor")
