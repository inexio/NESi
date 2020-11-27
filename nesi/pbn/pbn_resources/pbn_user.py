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

from nesi.softbox.base_resources.user import User, UserCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class PBNUser(User):
    """Represents a logical User resource"""

    level = base.Field('level')
    profile = base.Field('profile')
    
    def set_online(self):
        self.update(status='online')

    def set_offline(self):
        self.update(status='offline')
        

class PBNUserCollection(UserCollection):
    """Represent the collection of Users."""

    @property
    def _resource_type(self):
        return PBNUser
