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
from nesi.devices.edgecore.edgecore_resources import *

from nesi.devices.softbox.base_resources import credentials
from nesi.devices.softbox.base_resources.box import *

LOG = logging.getLogger(__name__)


class EdgeCoreBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """
    # Define Edgecore Properties
    management_start_address = base.Field('management_start_address')
    management_end_address = base.Field('management_end_address')
    logging_host = base.Field('logging_host')
    logging_port = base.Field('logging_port')
    logging_level = base.Field('logging_level')
    loopback_detection_action = base.Field('loopback_detection_action')
    sntp_server_ip = base.Field('sntp_server_ip')
    sntp_client = base.Field('sntp_client')
    timezone_name = base.Field('timezone_name')
    timezone_time = base.Field('timezone_time')
    summer_time_name = base.Field('summer_time_name')
    summer_time_region = base.Field('summer_time_region')

    @property
    def credentials(self):
        """Return `CredentialsCollection` object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    @property
    def users(self):
        """Return `UserCollection` object."""
        return edgecore_user.UserCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'users'))

    def get_user(self, field, value):
        """Get specific user object."""
        return edgecore_user.EdgecoreUserCollection(
            self._conn, base.get_sub_resource_path_by(self, 'users'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def cards(self):
        """Return `CardCollection` object."""
        return edgecore_card.EdgeCoreCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'))

    def get_card(self, field, value):
        """Get specific card object."""
        return edgecore_card.EdgeCoreCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value}).find_by_field_value(field, value)

    def get_cards(self, field, value):
        """Get all cards."""
        return edgecore_card.EdgeCoreCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value})

    @property
    def ports(self):
        """Return `PortCollection` object."""
        return edgecore_port.EdgeCorePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))

    def get_port(self, field, value):
        """Get specific port object."""
        return edgecore_port.EdgeCorePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_ports(self, field, value):
        """Get specific port object."""
        return edgecore_port.EdgeCorePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value})

    @property
    def interfaces(self):
        """Return `InterfaceCollection` object."""
        return edgecore_interface.EdgeCoreInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'))

    def get_interface(self, field, value):
        """Get specific interface object."""
        return edgecore_interface.EdgeCoreInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'),
            params={field: value}).find_by_field_value(field, value)

    def get_interfaces(self, field, value):
        """Get specific interface object."""
        return edgecore_interface.EdgeCoreInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'),
            params={field: value})

    @property
    def vlans(self):
        """Return `VlanCollection` object."""
        return edgecore_vlan.EdgeCoreVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'))

    def get_vlan(self, field, value):
        """Get specific vlan object."""
        return edgecore_vlan.EdgeCoreVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params={field: value}).find_by_field_value(field, value)

    def get_vlans(self, field, value):
        """Get specific vlan object."""
        return edgecore_vlan.EdgeCoreVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params={field: value})

    def add_vlan(self, **fields):
        """Add new vlan."""
        edgecore_vlan.EdgeCoreVlan.create(
            self._conn,
            os.path.join(self.path, 'vlans'),
            **fields
        )

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class EdgeCoreBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return EdgeCoreBox
