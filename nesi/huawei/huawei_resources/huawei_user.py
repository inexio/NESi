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

from nesi.softbox.base_resources.user import User, UserCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiUser(User):
    """Represents a logical User resource"""

    level = base.Field('level')
    profile = base.Field('profile')
    append_info = base.Field('append_info')
    reenter_num = base.Field('reenter_num')
    reenter_num_temp = base.Field('reenter_num_temp')

    def set_online(self):
        self.update(status='online')

    def set_offline(self):
        self.update(status='offline')

    def lock(self):
        self.update(lock_status='locked')

    def unlock(self):
        self.update(lock_status='unlocked')

    def set_reenter_num_temp(self, num):
        self.update(reenter_num_temp=num)


class HuaweiUserCollection(UserCollection):
    """Represent the collection of Users."""

    @property
    def _resource_type(self):
        return HuaweiUser
