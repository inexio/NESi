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

from nesi.huawei.huawei_resources import *

from nesi.softbox.base_resources import credentials
from nesi.softbox.base_resources import route
from nesi.softbox.base_resources.box import BoxCollection, Box, logging, base, os

LOG = logging.getLogger(__name__)


class HuaweiBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """
    cpu_occupancy = base.Field('cpu_occupancy')
    raio_anid = base.Field('raio_anid')
    handshake_mode = base.Field('handshake_mode')
    handshake_interval = base.Field('handshake_interval')
    interactive_mode = base.Field('interactive_mode')
    pitp = base.Field('pitp')
    pitp_mode = base.Field('pitp_mode')
    dsl_mode = base.Field('dsl_mode')

    @property
    def credentials(self):
        """Return `CredentialsCollection` object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    @property
    def users(self):
        """Return `UserCollection` object."""
        return huawei_user.HuaweiUserCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'users'))

    @property
    def routes(self):
        """Return `RouteCollection` object."""
        return route.RouteCollection(
            self._conn, base.get_sub_resource_path_by(self, 'routes'))

    @property
    def vlans(self):
        """Return `VlanCollection` object."""
        return huawei_vlan.HuaweiVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'))

    @property
    def port_profiles(self):
        """Return `PortProfileCollection` object."""
        return huawei_port_profile.HuaweiPortProfileCollection(
            self._conn, base.get_sub_resource_path_by(self, 'port_profiles'))

    @property
    def subracks(self):
        """Return `PortCollection` object."""
        return huawei_subrack.HuaweiSubrackCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subracks'))

    @property
    def cards(self):
        """Return `CardCollection` object."""
        return huawei_card.HuaweiCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'))

    @property
    def ports(self):
        """Return `PortCollection` object."""
        return huawei_port.HuaweiPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))

    @property
    def service_ports(self):
        """Return `ServicePortCollection` object."""
        return huawei_service_port.HuaweiServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'))

    @property
    def service_vlans(self):
        """Return `ServiceVlanCollection` object."""
        return huawei_service_vlan.HuaweiServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'))

    @property
    def onts(self):
        """Return `OntCollection` object."""
        return huawei_ont.HuaweiOntCollection(
            self._conn, base.get_sub_resource_path_by(self, 'onts'))

    @property
    def ont_ports(self):
        """Return `OntPortCollection` object."""
        return huawei_ont_port.HuaweiOntPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ont_ports'))

    @property
    def cpes(self):
        """Return `CpeCollection` object."""
        return huawei_cpe.HuaweiCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'))

    @property
    def cpe_ports(self):
        """Return `CpePortCollection` object."""
        return huawei_cpe_port.HuaweiCpePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpe_ports'))

    @property
    def emus(self):
        """Return `CpePortCollection` object."""
        return huawei_emu.HuaweiEmuCollection(
            self._conn, base.get_sub_resource_path_by(self, 'emus'))

    @property
    def vlan_interfaces(self):
        """Return `VlanInterfaceCollection` object."""
        return huawei_vlan_interface.HuaweiVlanInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlan_interfaces'))

    def get_user(self, field, value):
        """Get specific user object."""
        return huawei_user.HuaweiUserCollection(
            self._conn, base.get_sub_resource_path_by(self, 'users'),
            params={field: value}).find_by_field_value(field, value)

    def get_users(self, field, value):
        """Get specific user objects."""
        return huawei_user.HuaweiUserCollection(
            self._conn, base.get_sub_resource_path_by(self, 'users'),
            params={field: value})

    def get_credentials(self, field, value):
        """Get specific user object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(self, 'credentials'),
            params={field: value}).find_by_field_value(field, value)
    
    def get_subrack(self, field, value):
        """Get specific subrack object."""
        return huawei_subrack.HuaweiSubrackCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subracks'),
            params={field: value}).find_by_field_value(field, value)

    def get_card(self, field, value):
        """Get specific card object."""
        return huawei_card.HuaweiCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value}).find_by_field_value(field, value)

    def get_cards(self, field, value):
        """Get all cards."""
        return huawei_card.HuaweiCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value})

    def get_port(self, field, value):
        """Get specific port object."""
        return huawei_port.HuaweiPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_ports(self, field, value):
        """Get specific port object."""
        return huawei_port.HuaweiPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value})

    def get_service_port(self, field, value):
        """Get specific service-port object."""
        return huawei_service_port.HuaweiServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_service_port_by_values(self, params=None):
        """Get specific service_port object."""
        vlans = huawei_service_port.HuaweiServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params=params)

        # A collection is a non-subscriptable object, therefore we can only get the first object via this way
        if len(vlans) > 0:
            for vlan in vlans:
                return vlan
        else:
            return None

    def get_ont(self, field, value):
        """Get specific ont object."""
        return huawei_ont.HuaweiOntCollection(
            self._conn, base.get_sub_resource_path_by(self, 'onts'),
            params={field: value}).find_by_field_value(field, value)

    def get_onts(self, field, value):
        """Get specific ont object."""
        return huawei_ont.HuaweiOntCollection(
            self._conn, base.get_sub_resource_path_by(self, 'onts'),
            params={field: value})

    def get_ont_port(self, field, value):
        """Get specific ont_port object."""
        return huawei_ont_port.HuaweiOntPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ont_ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_ont_ports(self, field, value):
        """Get specific ont_port object."""
        return huawei_ont_port.HuaweiOntPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ont_ports'),
            params={field: value})

    def get_cpe(self, field, value):
        """Get specific cpe object."""
        return huawei_cpe.HuaweiCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'),
            params={field: value}).find_by_field_value(field, value)

    def get_cpes(self, field, value):
        """Get specific cpe object."""
        return huawei_cpe.HuaweiCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'),
            params={field: value})

    def get_cpe_port(self, field, value):
        """Get specific cpe_port object."""
        return huawei_cpe_port.HuaweiCpePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpe_ports'),
            params={field: value}).find_by_field_value(field, value)

    def get_cpe_ports(self, field, value):
        """Get specific cpe_port object."""
        return huawei_cpe_port.HuaweiCpePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpe_ports'),
            params={field: value})

    def get_emu(self, field, value):
        """Get specific emu object."""
        return huawei_emu.HuaweiEmuCollection(
            self._conn, base.get_sub_resource_path_by(self, 'emus'),
            params={field: value}).find_by_field_value(field, value)

    def get_vlan(self, field, value):
        """Get specific vlan object."""
        return huawei_vlan.HuaweiVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params={field: value}).find_by_field_value(field, value)

    def get_vlan_by_values(self, params=None):
        """Get specific vlan object."""
        vlans = huawei_vlan.HuaweiVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params=params)

        # A collection is a non-subscriptable object, therefore we can only get the first object via this way
        if len(vlans) > 0:
            for vlan in vlans:
                return vlan
        else:
            return None

    def get_vlan_interface(self, field, value):
        """Get specific vlan interface object."""
        return huawei_vlan_interface.HuaweiVlanInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlan_interfaces'),
            params={field: value}).find_by_field_value(field, value)

    def get_port_profile(self, field, value):
        """Get specific port_profile object."""
        return huawei_port_profile.HuaweiPortProfileCollection(
            self._conn, base.get_sub_resource_path_by(self, 'port_profiles'),
            params={field: value}).find_by_field_value(field, value)

    def get_service_vlan(self, field, value):
        """Get specific service-vlan object."""
        return huawei_service_vlan.HuaweiServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params={field: value}).find_by_field_value(field, value)

    def get_service_vlan_by_values(self, params=None):
        """Get specific service-vlan object."""
        service_vlans = huawei_service_vlan.HuaweiServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params=params)

        # A collection is a non-subscriptable object, therefore we can only get the first object via this way
        if len(service_vlans) > 0:
            for service_vlan in service_vlans:
                return service_vlan
        else:
            return None

    def add_credentials(self, **fields):
        """Add a new pair of credentials"""
        return credentials.Credentials.create(
            self._conn,
            os.path.join(self.path, 'credentials'),
            **fields
        )

    def add_user(self, **fields):
        """Add a new user"""
        return huawei_user.HuaweiUser.create(
            self._conn,
            os.path.join(self.path, 'users'),
            **fields
        )

    def add_vlan(self, **fields):
        """Add new vlan."""
        huawei_vlan.HuaweiVlan.create(
            self._conn,
            os.path.join(self.path, 'vlans'),
            **fields
        )

    def add_ont(self, **fields):
        """Add new ont."""
        return huawei_ont.HuaweiOnt.create(
                self._conn,
                os.path.join(self.path, 'onts'),
                **fields)

    def add_ont_port(self, **fields):
        """Add new ont."""
        return huawei_ont_port.HuaweiOntPort.create(
                self._conn,
                os.path.join(self.path, 'ont_ports'),
                **fields)

    def add_service_port(self, **fields):
        """Add a new service port"""
        return huawei_service_port.HuaweiServicePort.create(
            self._conn,
            os.path.join(self.path, 'service_ports'),
            **fields
        )

    def add_service_vlan(self, **fields):
        """Add a new service vlan"""
        return huawei_service_vlan.HuaweiServiceVlan.create(
            self._conn,
            os.path.join(self.path, 'service_vlans'),
            **fields
        )

    def add_vlan_interface(self, **fields):
        """Add a new vlan interface"""
        return huawei_vlan_interface.HuaweiVlanInterface.create(
            self._conn,
            os.path.join(self.path, 'vlan_interfaces'),
            **fields
        )

    def add_route(self, **fields):
        """Add a new route"""
        return huawei_route.HuaweiRoute.create(
            self._conn,
            os.path.join(self.path, 'routes'),
            **fields
        )

    def add_port_profile(self, **fields):
        """Add a new port profile"""
        return huawei_port_profile.HuaweiPortProfile.create(
            self._conn,
            os.path.join(self.path, 'port_profiles'),
            **fields
        )

    def set_network_address(self, addr):
        """Change the hostname of a box"""
        self.update(network_address=addr)

    def set_raio_anid(self, addr):
        """Change the raio anid of a box"""
        self.update(raio_anid=addr)

    def set_handshake_mode(self, mode):
        """Change the handshake mode of a box"""
        self.update(handshake_mode=mode)

    def set_handshake_interval(self, interval):
        """Change the handshake interval of a box"""
        self.update(handshake_interval=interval)

    def disable_interactive(self):
        """Disable Interactive function."""
        self.update(interactive_mode=False)

    def enable_interactive(self):
        """Enable Interactive function."""
        self.update(interactive_mode=True)

    def set_dsl_mode(self, mode):
        """Change the dsl mode of a box"""
        self.update(dsl_mode=mode)


    def set_pitp(self, state):
        """Change the pitp of a box"""
        self.update(pitp=state)

    def set_pitp_mode(self, mode):
        """Change the pitp mode of a box"""
        self.update(pitp_mode=mode)

class HuaweiBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return HuaweiBox
