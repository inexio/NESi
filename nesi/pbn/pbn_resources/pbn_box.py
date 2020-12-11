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

from nesi.pbn.pbn_resources import *
import logging
from nesi.softbox.base_resources import credentials, base
from nesi.softbox.base_resources.box import Box, BoxCollection

LOG = logging.getLogger(__name__)


class PBNBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """

    @property
    def credentials(self):
        """Return `CredentialsCollection` object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    def get_credentials(self, field, value):
        """Get specific user object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(self, 'credentials'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def users(self):
        """Return `UserCollection` object."""
        return pbn_user.PBNUserCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'users'))

    def get_user(self, field, value):
        """Get specific user object."""
        return pbn_user.PBNUserCollection(
            self._conn, base.get_sub_resource_path_by(self, 'users'),
            params={field: value}).find_by_field_value(field, value)

    def get_users(self, field, value):
        """Get specific user objects."""
        return pbn_user.PBNUserCollection(
            self._conn, base.get_sub_resource_path_by(self, 'users'),
            params={field: value})

    @property
    def vlans(self):
        """Return `VlanCollection` object."""
        return pbn_vlan.PBNVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'))

    def get_vlan(self, field, value):
        """Get specific vlan object."""
        return pbn_vlan.PBNVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def service_ports(self):
        """Return `ServicePortCollection` object."""
        return pbn_service_port.PBNServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'))

    def get_service_port(self, field, value):
        """Get specific service-port object."""
        return pbn_service_port.PBNServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_service_ports_by_values(self, params):
        """Get a collection of service port objects."""
        return pbn_service_port.PBNServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params=params)

    @property
    def service_vlans(self):
        """Return `ServiceVlanCollection` object."""
        return pbn_service_vlan.PBNServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'))

    def get_service_vlan(self, field, value):
        """Get specific service-vlan object."""
        return pbn_service_vlan.PBNServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def cards(self):
        """Return `cardCollection` object."""
        return pbn_card.PBNCardCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'cards'))

    def get_card(self, field, value):
        """Get specific card object."""
        return pbn_card.PBNCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def ports(self):
        """Return `PortCollection` object."""
        return pbn_port.PBNPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))

    def get_port(self, field, value):
        """Get specific port object."""
        return pbn_port.PBNPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)


class PBNBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return PBNBox
