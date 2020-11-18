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

from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class Credentials(base.Resource):
    """Represent user credentials."""

    id = base.Field('id')
    user_id = base.Field('user_id')
    protocol = base.Field('protocol')
    username = base.Field('username')
    password = base.Field('password')


class CredentialsCollection(base.ResourceCollection):
    """Represent a collection of users credentials."""

    @property
    def _resource_type(self):
        return Credentials
