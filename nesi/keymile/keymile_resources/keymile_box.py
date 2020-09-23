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

from nesi.keymile.keymile_resources import keymile_card
from nesi.softbox.base_resources import credentials
from nesi.softbox.base_resources.box import *

LOG = logging.getLogger(__name__)


class KeyMileBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """
    # Define Keymile Properties

    @property
    def credentials(self):
        """Return `CredentialsCollection` object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    @property
    def cards(self):
        """Return `CredentialsCollection` object."""
        return keymile_card.KeyMileCardCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'cards'))


class KeyMileBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return KeyMileBox
