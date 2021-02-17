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


from nesi.devices.alcatel.alcatel_resources import *
import logging
from nesi.devices.softbox.base_resources import credentials, base
from nesi.devices.softbox.base_resources import user
from nesi.devices.softbox.base_resources import route
from nesi.devices.softbox.base_resources.box import Box, BoxCollection, os

LOG = logging.getLogger(__name__)


class AlcatelBox(Box):
    """Represent a network device (AKA box).

    :param connection: A RestClient instance
    :param identity: The identity of the System resource
    """

    contact_person = base.Field('contact_person')
    isam_id = base.Field('isam_id')
    isam_location = base.Field('isam_location')
    board_missing_reporting_logging = base.Field('board_missing_reporting_logging')
    board_instl_missing_reporting_logging = base.Field('board_instl_missing_reporting_logging')
    board_init_reporting_logging = base.Field('board_init_reporting_loggin')
    board_hw_issue_reporting_logging = base.Field('board_hw_issue_reporting_logging')
    plugin_dc_b_severity = base.Field('plugin_dc_b_severity')
    logging_server_ip = base.Field('logging_server_ip')
    udp_logging_server_ip = base.Field('udp_logging_server_ip')
    syslog_route = base.Field('syslog_route')
    public_host_address = base.Field('public_host_address')
    futurama_host_address = base.Field('futurama_host_address')
    tellme_host_address = base.Field('tellme_host_address')
    disk_space = base.Field('disk_space')
    free_space = base.Field('free_space')
    download_progress = base.Field('download_progress')
    download_error = base.Field('download_error')
    upload_progress = base.Field('upload_progress')
    upload_error = base.Field('upload_error')
    auto_activate_error = base.Field('auto_activate_error')
    max_lt_link_speed = base.Field('max_lt_link_speed')
    port_num_in_proto = base.Field('port_num_in_proto')
    admin_slot_numbering = base.Field('admin_slot_numbering')
    default_routes = base.Field('default_routes')
    primary_file_server_id = base.Field('primary_file_server_id')
    broadcast_frames = base.Field('broadcast_frames')
    priority_policy_port_default = base.Field('priority_policy_port_default')
    sntp_server_table = base.Field('sntp_server_table')

    @property
    def credentials(self):
        """Return `CredentialsCollection` object."""
        return credentials.CredentialsCollection(
            self._conn, base.get_sub_resource_path_by(
                self, 'credentials'))

    @property
    def users(self):
        """Return `UserCollection` object."""
        return user.UserCollection(
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
        return alcatel_vlan.AlcatelVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'))

    def add_vlan(self, **fields):
        """Add new vlan."""
        return alcatel_vlan.AlcatelVlan.create(
            self._conn,
            os.path.join(self.path, 'vlans'),
            **fields
        )

    def get_vlan(self, field, value):
        """Get specific vlan object."""
        return alcatel_vlan.AlcatelVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'vlans'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def service_vlans(self):
        """Return `ServiceVlanCollection` object."""
        return alcatel_service_vlan.AlcatelServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'))

    def add_service_vlan(self, **fields):
        """Add a new service vlan"""
        return alcatel_service_vlan.AlcatelServiceVlan.create(
            self._conn,
            os.path.join(self.path, 'service_vlans'),
            **fields
        )

    def get_service_vlan_by_values(self, params=None):
        """Get specific service-vlan object."""
        service_vlans = alcatel_service_vlan.AlcatelServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params=params)

        # A collection is a non-subscriptable object, therefore we can only get the first object via this way
        if len(service_vlans) > 0:
            for service_vlan in service_vlans:
                return service_vlan
        else:
            return None

    def get_service_vlan(self, field, value):
        """Get specific service-vlan object."""
        return alcatel_service_vlan.AlcatelServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params={field: value}).find_by_field_value(field, value)

    def get_service_vlans(self, field, value):
        """Get specific service-vlan object collection."""
        return alcatel_service_vlan.AlcatelServiceVlanCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_vlans'),
            params={field: value})

    def get_service_vlans_by_service_port_id(self, service_port_id):
        """Get all service-vlans for a specific service-port"""
        return self.get_service_vlans('service_port_id', service_port_id)

    @property
    def port_profiles(self):
        """Return `PortProfileCollection` object."""
        return alcatel_port_profile.AlcatelPortProfileCollection(
            self._conn, base.get_sub_resource_path_by(self, 'port_profiles'))

    def get_port_profile(self, field, value):
        """Get specific port_profile object."""
        return alcatel_port_profile.AlcatelPortProfileCollection(
            self._conn, base.get_sub_resource_path_by(self, 'port_profiles'),
            params={field: value}).find_by_field_value(field, value)

    def get_port_profiles(self, params=None):
        """Get all port profiles."""
        return alcatel_port_profile.AlcatelPortProfileCollection(
            self._conn, base.get_sub_resource_path_by(self, 'port_profiles'),
            params=params)

    @property
    def subracks(self):
        """Return `PortCollection` object."""
        return alcatel_subrack.AlcatelSubrackCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subracks'))

    def get_subrack(self, field, value):
        """Get specific subrack object."""
        return alcatel_subrack.AlcatelSubrackCollection(
            self._conn, base.get_sub_resource_path_by(self, 'subracks'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def cards(self):
        """Return `CardCollection` object."""
        return alcatel_card.AlcatelCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'))

    def get_card(self, field, value):
        """Get specific card object."""
        return alcatel_card.AlcatelCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params={field: value}).find_by_field_value(field, value)

    def get_cards(self, params=None):
        """Get all cards."""
        return alcatel_card.AlcatelCardCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cards'),
            params=params)

    @property
    def ports(self):
        """Return `PortCollection` object."""
        return alcatel_port.AlcatelPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'))

    def get_port(self, field, value):
        """Get specific port object."""
        return alcatel_port.AlcatelPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ports'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def service_ports(self):
        """Return `ServicePortCollection` object."""
        return alcatel_service_port.AlcatelServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'))

    def add_service_port(self, **fields):
        """Add a new service port"""
        return alcatel_service_port.AlcatelServicePort.create(
            self._conn,
            os.path.join(self.path, 'service_ports'),
            **fields
        )

    def get_service_port(self, field, value):
        """Get specific service-port object."""
        return alcatel_service_port.AlcatelServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def qos_interfaces(self):
        """Return `QosInterfaceCollection` object."""
        return alcatel_qos_interface.AlcatelQosInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'qos_interfaces'))

    def add_qos_interface(self, **fields):
        """Add a new qos interface"""
        return alcatel_qos_interface.AlcatelQosInterface.create(
            self._conn,
            os.path.join(self.path, 'qos_interfaces'),
            **fields
        )

    def get_qos_interface(self, field, value):
        """Get specific qos_interface object."""
        return alcatel_qos_interface.AlcatelQosInterfaceCollection(
            self._conn, base.get_sub_resource_path_by(self, 'qos_interfaces'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def onts(self):
        """Return `OntCollection` object."""
        return alcatel_ont.AlcatelOntCollection(
            self._conn, base.get_sub_resource_path_by(self, 'onts'))

    def get_ont(self, field, value):
        """Get specific ont object."""
        return alcatel_ont.AlcatelOntCollection(
            self._conn, base.get_sub_resource_path_by(self, 'onts'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def ont_ports(self):
        """Return `OntPortCollection` object."""
        return alcatel_ont_port.AlcatelOntPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ont_ports'))

    def get_ont_port(self, field, value):
        """Get specific ont_port object."""
        return alcatel_ont_port.AlcatelOntPortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'ont_ports'),
            params={field: value}).find_by_field_value(field, value)

    @property
    def cpes(self):
        """Return `CpeCollection` object."""
        return alcatel_cpe.AlcatelCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'))

    def get_cpe(self, field, value):
        """Get specific cpe object."""
        return alcatel_cpe.AlcatelCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'),
            params={field: value}).find_by_field_value(field, value)

    def get_cpes(self, field, value):
        """Get specific cpe object collection."""
        return alcatel_cpe.AlcatelCpeCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpes'),
            params={field: value})

    @property
    def cpe_ports(self):
        """Return `CpePortCollection` object."""
        return alcatel_cpe_port.AlcatelCpePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpe_ports'))

    def get_cpe_port(self, field, value):
        """Get specific cpe_port object."""
        return alcatel_cpe_port.AlcatelCpePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'cpe_ports'),
            params={field: value}).find_by_field_value(field, value)

#########################################################################

    def get_service_port_by_values(self, params=None):
        """Get specific service_port object."""
        vlans = alcatel_service_port.AlcatelServicePortCollection(
            self._conn, base.get_sub_resource_path_by(self, 'service_ports'),
            params=params)

        # A collection is a non-subscriptable object, therefore we can only get the first object via this way
        if len(vlans) > 0:
            for vlan in vlans:
                return vlan
        else:
            return None

    def set_contact_person(self, contact_person):
        """Change contact person of a box."""
        self.update(contact_person=contact_person)

    def set_login_banner(self, login_banner):
        """Set the login banner of a box."""
        self.update(login_banner=login_banner)

    def set_welcome_banner(self, welcome_banner):
        """Set the welcome banner of a box."""
        self.update(welcome_banner=welcome_banner)

    def set_isam_id(self, isam_id):
        """Change isam id of a box."""
        self.update(isam_id=isam_id)

    def set_isam_location(self, isam_location):
        """Change isam location of a box."""
        self.update(isam_location=isam_location)

    def set_board_missing_reporting_logging(self, bool):
        """Change borad missing alarm value."""
        self.update(board_missing_reporting_logging=bool)

    def set_board_instl_missing_reporting_logging(self, bool):
        """Change borad missing alarm value."""
        self.update(board_instl_missing_reporting_logging=bool)

    def set_board_init_reporting_logging(self, bool):
        """Change borad missing alarm value."""
        self.update(board_init_reporting_logging=bool)

    def set_board_hw_issue_reporting_logging(self, bool):
        """Change borad missing alarm value."""
        self.update(board_hw_issue_reporting_logging=bool)

    def set_plugin_dc_b_severity(self, bool):
        """Change plugin_dc_b_severity alarm value."""
        self.update(plugin_dc_b_severity=bool)

    def set_logging_server_ip(self, address):
        """Change syslog_destination value."""
        self.update(logging_server_ip=address)

    def set_udp_logging_server_ip(self, address):
        """Change loggingServerIp value."""
        self.update(udp_logging_server_ip=address)

    def set_syslog_route(self, route):
        """Change syslog_route value."""
        self.update(syslog_route=route)

    def set_public_host_address(self, address):
        """Change public_host_address value."""
        self.update(public_host_address=address)

    def set_futurama_host_address(self, address):
        """Change futurama_host_address value."""
        self.update(futurama_host_address=address)

    def set_tellme_host_address(self, address):
        """Change tellme_host_address value."""
        self.update(tellme_host_address=address)

    def set_upload_progress(self, upload_progress):
        """Change upload_progress value."""
        self.update(upload_progress=upload_progress)

    def set_max_lt_link_speed(self, link_speed):
        """Change max_lt_link_speed value."""
        self.update(max_lt_link_speed=link_speed)

    def set_port_num_in_proto(self, port_num):
        """Change port_num_in_proto value."""
        self.update(port_num_in_proto=port_num)

    def set_admin_slot_numbering(self, number):
        """Change admin_slot_numbering value."""
        self.update(admin_slot_numbering=number)

    def set_default_route(self, default_route):
        """Change default_route"""
        self.update(default_route=default_route)

    def set_mgmt_address(self, mgmt_address):
        """Change default_route"""
        self.update(mgmt_address=mgmt_address)

    def set_primary_file_server_id(self, address):
        """Change primary_file_server_id value"""
        self.update(primary_file_server_id=address)

    def set_broadcast_frames(self, broadcast_frames):
        """Change broadcast_frames value"""
        self.update(broadcast_frames=broadcast_frames)

    def set_priority_policy_port_default(self, priority_policy_port_default):
        """Change priority_policy_port_default value"""
        self.update(priority_policy_port_default=priority_policy_port_default)

    def set_sntp_server_table(self, ip):
        """Add an Ip address to the sntp server table"""
        self.update(sntp_server_table=ip)


class AlcatelBoxCollection(BoxCollection):
    """Represent a collection of boxen.

    :param connection: A RestClient instance
    :param path: The canonical path to the Box collection resource
    """

    @property
    def _resource_type(self):
        return AlcatelBox
