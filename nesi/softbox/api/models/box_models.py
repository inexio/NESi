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
import uuid
import datetime

from nesi.softbox.api import db
from .credential_models import Credential
from .subrack_models import Subrack
from .card_models import Card
from .port_models import Port
from .cpe_models import Cpe
from .cpeport_models import CpePort
from .ont_models import Ont
from .ontport_models import OntPort
from .portprofile_models import PortProfile
from .vlan_models import Vlan
from .vlan_interface_models import VlanInterface
from .route_models import Route
from .emu_models import Emu
from .user_models import User


class Box(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    vendor = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    version = db.Column(db.String(64), nullable=False)
    software_version = db.Column(db.String(64), nullable=False)
    network_protocol = db.Column(db.Enum('telnet', 'ssh'), default='telnet')
    network_port = db.Column(db.Integer(), default=None)
    network_address = db.Column(db.String(), default=None)
    uuid = db.Column(
        db.String(36), nullable=False, unique=True,
        default=lambda: str(uuid.uuid1()))
    description = db.Column(db.String())
    hostname = db.Column(db.String(64))
    mgmt_address = db.Column(db.String(32))
    contact_person = db.Column(db.String(), default=None, nullable=True)
    isam_id = db.Column(db.String(), default=None, nullable=True)
    isam_location = db.Column(db.String(), default=None, nullable=True)
    login_banner = db.Column(db.String(), default="")
    welcome_banner = db.Column(db.String, default="")
    credentials = db.relationship('Credential', backref='Box', lazy='dynamic')
    credential_details = db.relationship('Credential', backref='credentials', lazy='dynamic')
    users = db.relationship('User', backref='Box', lazy='dynamic')
    subracks = db.relationship('Subrack', backref='Box', lazy='dynamic')
    subrack_details = db.relationship('Subrack', backref='subracks', lazy='dynamic')
    cards = db.relationship('Card', backref='Box', lazy='dynamic')
    ports = db.relationship('Port', backref='Box', lazy='dynamic')
    cpes = db.relationship('Cpe', backref='Box', lazy='dynamic')
    cpe_ports = db.relationship('CpePort', backref='Box', lazy='dynamic')
    onts = db.relationship('Ont', backref='Box', lazy='dynamic')
    ont_ports = db.relationship('OntPort', backref='Box', lazy='dynamic')
    port_profiles = db.relationship('PortProfile', backref='Box', lazy='dynamic')
    port_profile_details = db.relationship('PortProfile', backref='port_profiles', lazy='dynamic')
    vlans = db.relationship('Vlan', backref='Box', lazy='dynamic')
    vlan_details = db.relationship('Vlan', backref='vlans', lazy='dynamic')
    vlan_interfaces = db.relationship('VlanInterface', backref='Box', lazy='dynamic')
    routes = db.relationship('Route', backref='Box', lazy='dynamic')
    emus = db.relationship('Emu', backref='Box', lazy='dynamic')
    board_missing_reporting_logging = db.Column(db.Boolean(), default=False)
    board_instl_missing_reporting_logging = db.Column(db.Boolean(), default=False)
    board_init_reporting_logging = db.Column(db.Boolean(), default=False)
    board_hw_issue_reporting_logging = db.Column(db.Boolean(), default=False)
    plugin_dc_b_severity = db.Column(db.Boolean(), default=False)
    sntp_server_ip_address = db.Column(db.String(), default='')
    sntp_server_table = db.Column(db.String(), default='')
    timezone_offset = db.Column(db.String())
    last_login = db.Column(db.String(), default='/')
    last_logout = db.Column(db.String(), default='/')
    logging_server_ip = db.Column(db.String(), default='')
    udp_logging_server_ip = db.Column(db.String(), default='')
    syslog_route = db.Column(db.String(), default='')
    public_host_address = db.Column(db.String(), default='')
    futurama_host_address = db.Column(db.String(), default='')
    tellme_host_address = db.Column(db.String(), default='')
    max_lt_link_speed = db.Column(db.String(), default='')
    port_num_in_proto = db.Column(db.Enum('type-based', 'legacy-num', 'position-based'))
    admin_slot_numbering = db.Column(db.String(), default='')
    primary_file_server_id = db.Column(db.String(), default='')
    disk_space = db.Column(db.Integer(), nullable=False, default=574423552)
    free_space = db.Column(db.Integer(), default=420016640)
    download_progress = db.Column(db.Enum('download-fail', 'download-ongoing', 'download-success'),
                                  default='download-success')
    download_error = db.Column(db.Enum('no-error', 'error'), default='no-error')
    upload_progress = db.Column(db.Enum('upload-fail', 'upload-ongoing', 'upload-success'), default='upload-success')
    upload_error = db.Column(db.Enum('no-error', 'error'), default='no-error')
    auto_activate_error = db.Column(db.Enum('no-error', 'error'), default='no-error')
    default_route = db.Column(db.String(), default=None)
    broadcast_frames = db.Column(db.Boolean(), default=False)
    priority_policy_port_default = db.Column(db.Boolean(), default=False)

    cpu_occupancy = db.Column(db.String(), default='20%')
    raio_anid = db.Column(db.String(), default='127.0.0.1')
    handshake_mode = db.Column(db.Enum('enable', 'disable'), default='disable')
    handshake_interval = db.Column(db.Integer(), default=None)
    interactive_mode = db.Column(db.Boolean(), default=True)
