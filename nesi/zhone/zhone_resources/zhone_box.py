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
from nesi.zhone.zhone_resources import *

from nesi.softbox.base_resources import credentials, base
from nesi.softbox.base_resources import route
from nesi.softbox.base_resources.box import *

LOG = logging.getLogger(__name__)


class ZhoneBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """
    # Define Zhone Properties
    @property
    def credentials(self):
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    def get_port(self, field, value):
        """Get specific port object."""
        return zhone_port.ZhonePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)



class ZhoneBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return ZhoneBox
