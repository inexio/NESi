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
import os

from nesi.keymile.keymile_resources import *

from nesi.softbox.base_resources import credentials, base
from nesi.softbox.base_resources.box import BoxCollection, Box, logging

LOG = logging.getLogger(__name__)


class KeyMileBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """

    currTemperature = base.Field("currTemperature")
    backup_ip = base.Field("backup_ip")
    login = base.Field("login")
    password = base.Field("password")
    backup_path = base.Field("backup_path")

    def set_backup(self, backup_ip, login, password):
        self.update(backup_ip=backup_ip)
        self.update(login=login)
        self.update(password=password)

    def set_path(self, path):
        self.update(backup_path=path)

    @property
    def channels(self):
        """Return `ChannelCollection` object."""
        return keymile_channel.KeyMileChannelCollection(
            self._conn, base.get_sub_resource_path_by(self, 'channels'))

    @property
    def interfaces(self):
        """Return `InterfaceCollection` object."""
        return keymile_interface.KeyMileInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'))

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

    @property
    def subscribers(self):
        """Return `SubscriberCollection` object."""
        return keymile_subscriber.KeyMileSubscriberCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subscribers'))

    @property
    def portgroupsports(self):
        """Return `PortgrouportCollection` object."""
        return keymile_portgroupport.KeyMilePortGroupPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'portgrouports'))

    def logports(self):
        """Return `LogPortCollection` object."""
        return keymile_logport.KeyMileLogPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'logports'))

    @property
    def srvcs(self):
        """Return `SrvcCollection` object."""
        return keymile_srvc.KeyMileSrvcCollection(
            self._conn, base.get_sub_resource_path_by(self, 'srvcs'))

    def get_card(self, field, value):
        """Get specific card object."""
        return keymile_card.KeyMileCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value}).find_by_field_value(field, value)

    def get_cards(self, field, value):
        """Get all cards."""
        return keymile_card.KeyMileCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value})

    def get_port(self, field, value):
        """Get specific port object."""
        return keymile_port.KeyMilePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_ports(self, field, value):
        """Get specific port object."""
        return keymile_port.KeyMilePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value})

    def get_logport(self, field, value):
        """Get specific logport object."""
        return keymile_logport.KeyMileLogPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'logports'),
            params={field: value}).find_by_field_value(field, value)

    def get_logports(self, field, value):
        """Get al logport objects with a specific trait."""
        return keymile_logport.KeyMileLogPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'logports'),
            params={field: value})

    def add_logport(self, **fields):
        """Add new logport."""
        return keymile_logport.KeyMileLogPort.create(
                self._conn,
                os.path.join(self.path, 'logports'),
                **fields)

    def get_chan(self, field, value):
        """Get specific channel object."""
        return keymile_channel.KeyMileChannelCollection(
            self._conn, base.get_sub_resource_path_by(self, 'channels'),
            params={field: value}).find_by_field_value(field, value)

    def get_chans(self, field, value):
        return keymile_channel.KeyMileChannelCollection(
            self._conn, base.get_sub_resource_path_by(self, 'channels'),
            params={field: value})

    def get_interface(self, field, value):
        """Get specific interface object."""
        return keymile_interface.KeyMileInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'),
            params={field: value}).find_by_field_value(field, value)

    def get_interfaces(self, field, value):
        """Get specific interface object."""
        return keymile_interface.KeyMileInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'interfaces'),
            params={field: value})

    def add_interface(self, **fields):
        """Add new interface/vcc."""
        return keymile_interface.KeyMileInterface.create(
                self._conn,
                os.path.join(self.path, 'interfaces'),
                **fields)

    def get_subscriber(self, field, value):
        """Get specific subscriber object."""
        return keymile_subscriber.KeyMileSubscriberCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subscribers'),
            params={field: value}).find_by_field_value(field, value)

    def get_subscribers(self, field, value):
        """Get specific subscribers object."""
        return keymile_subscriber.KeyMileSubscriberCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subscribers'),
            params={field: value})

    def add_subscriber(self, **fields):
        """Add new subscriber."""
        return keymile_subscriber.KeyMileSubscriber.create(
                self._conn,
                os.path.join(self.path, 'subscribers'),
                **fields)

    def get_portgroupport(self, field, value):
        """Get specific portgroupport object."""
        return keymile_portgroupport.KeyMilePortGroupPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'portgroupports'),
            params={field: value}).find_by_field_value(field, value)

    def get_portgroupports(self, field, value):
        """Get specific portgroupports object."""
        return keymile_portgroupport.KeyMilePortGroupPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'portgroupports'),
            params={field: value})
    
    def get_srvc(self, field, value):
        """Get specific srvc object."""
        return keymile_srvc.KeyMileSrvcCollection(
            self._conn, base.get_sub_resource_path_by(self, 'srvcs'),
            params={field: value}).find_by_field_value(field, value)

    def get_srvcs(self, field, value):
        """Get specific srvcs object."""
        return keymile_srvc.KeyMileSrvcCollection(
            self._conn, base.get_sub_resource_path_by(self, 'srvcs'),
            params={field: value})

    def add_srvc(self, **fields):
        """Add new srvc."""
        return keymile_srvc.KeyMileSrvc.create(
                self._conn,
                os.path.join(self.path, 'srvcs'),
                **fields)


class KeyMileBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return KeyMileBox
