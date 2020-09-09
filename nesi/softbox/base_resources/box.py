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
import os
from nesi.softbox import base
from nesi.exceptions import PropertyNotFoundError
from nesi.exceptions import FunctionNotFoundError

LOG = logging.getLogger(__name__)


class Box(base.Resource):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """

    vendor = base.Field('vendor', required=True)
    """Network device vendor e.g. cisco"""

    model = base.Field('model', required=True)
    """Network device model e.g. 5300"""

    version = base.Field('version', required=True)
    """Network device model version e.g. 1.2.3"""

    network_protocol = base.Field('network_protocol', required=True)
    """Network device network protocol used by the daemon"""

    network_address = base.Field('network_address')
    """Network device network address used by the daemon"""

    network_port = base.Field('network_port')
    """Network device network port used by the daemon"""

    uuid = base.Field('uuid', required=True)
    """Network device unique instance ID"""

    description = base.Field('description')
    """The description of this box"""

    hostname = base.Field('hostname')
    """Network device model e.g. 5300"""

    mgmt_address = base.Field('mgmt_address')
    """Management IP address"""

    software_version = base.Field('software_version')
    """Software Version"""

    login_banner = base.Field('login_banner')
    """Login banner"""

    welcome_banner = base.Field('welcome_banner')
    """Welcome banner"""

    id = base.Field('id')
    last_login = base.Field('last_login')
    last_logout = base.Field('last_logout')
    timezone_offset = base.Field('timezone_offset')
    sntp_server_ip_address = base.Field('sntp_server_ip_address')

    def set_hostname(self, name):
        """Change the hostname value."""
        self.update(hostname=name)

    def set_last_login(self, time):
        """Change last_login value."""
        self.update(last_login=time)

    def set_last_logout(self, time):
        """Change last_login value."""
        self.update(last_logout=time)

    def set_timezone_offset(self, offset):
        """Change timezone_offset value."""
        self.update(timezone_offset=offset)

    def set_sntp_server_ip_address(self, address):
        """Change sntp_server_ip_address value."""
        self.update(sntp_server_ip_address=address)

    # define abstract properties

    @property
    def credentials(self):
        raise PropertyNotFoundError("abstract credentials properties")

    @property
    def users(self):
        raise PropertyNotFoundError("abstract users properties")

    @property
    def routes(self):
        raise PropertyNotFoundError("abstract routes properties")

    @property
    def vlans(self):
        raise PropertyNotFoundError("abstract vlans properties")

    @property
    def service_vlans(self):
        raise PropertyNotFoundError("abstract service_vlans properties")

    @property
    def vlans_connections(self):
        raise PropertyNotFoundError("abstract vlans properties")

    @property
    def port_profiles(self):
        raise PropertyNotFoundError("abstract port_profiles properties")

    @property
    def subracks(self):
        raise PropertyNotFoundError("abstract subracks properties")

    @property
    def cards(self):
        raise PropertyNotFoundError("abstract cards properties")

    @property
    def ports(self):
        raise PropertyNotFoundError("abstract ports properties")

    @property
    def service_ports(self):
        raise PropertyNotFoundError("abstract service_ports properties")

    @property
    def onts(self):
        raise PropertyNotFoundError("abstract onts properties")

    @property
    def ont_ports(self):
        raise PropertyNotFoundError("abstract ont_ports properties")

    @property
    def cpes(self):
        raise PropertyNotFoundError("abstract cpes properties")

    @property
    def cpe_ports(self):
        raise PropertyNotFoundError("abstract cpe_ports properties")

    def set_login_banner(self, login_banner):
        raise FunctionNotFoundError("abstract set_login_banner function")

    def set_welcome_banner(self, welcome_banner):
        raise FunctionNotFoundError("abstract set_welcome_banner function")


class BoxCollection(base.ResourceCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return Box
