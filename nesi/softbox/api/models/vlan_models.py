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

from nesi.softbox.api import db


class Vlan(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String())
    role = db.Column(
        db.Enum('access', 'trunk', 'native'),
        nullable=False, default='access')
    # data
    # pending is just a placeholder for status value
    status = db.Column(db.Enum('learned', 'pending'), default='learned')
    tag = db.Column(db.Enum('tagged', 'untagged', 'single-tagged'), default='untagged')
    egress_port = db.Column(db.String(), default='')
    fdb_id = db.Column(db.Integer, default=2620)
    shutdown = db.Column(db.Boolean(), default=False)
    mtu = db.Column(db.Integer(), default=1500)
    access_group_in = db.Column(db.String(64), default='')
    access_group_out = db.Column(db.String(64), default='')
    ip_redirect = db.Column(db.Boolean(), default=False)
    ip_proxy_arp = db.Column(db.Boolean(), default=False)
    unicast_reverse_path_forwarding = db.Column(db.Boolean(), default=False)
    load_interval = db.Column(db.Integer(), default=100)
    mpls_ip = db.Column(db.String(32), default='10.1.1.12')
    protocol_filter = db.Column(db.String(32), default=None)
    pppoe_relay_tag = db.Column(db.String(32), default=None)
    pppoe_linerate = db.Column(db.String(32), default=None)
    circuit_id_pppoe = db.Column(db.String(32), default=None)
    remote_id_pppoe = db.Column(db.String(32), default=None)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    in_qos_prof_name = db.Column(db.String(), default=None)
    new_broadcast = db.Column(db.Enum('enable', 'disable'), default='disable')
    new_secure_fwd = db.Column(db.Enum('enable', 'disable'), default='disable')
    dhcp_opt82 = db.Column(db.Enum('enable', 'disable'), default='disable')
    dhcp_opt82_ext = db.Column(db.Enum('enable', 'disable'), default='disable')
    aging_time = db.Column(db.Integer(), nullable=True)
    circuit_id_dhcp = db.Column(db.String(32), default=None)
    remote_id_dhcp = db.Column(db.String(32), default=None)
    mode = db.Column(db.Enum('residential-bridge', 'reserved'), default='residential-bridge')

    # Huawei Data
    type = db.Column(db.Enum('smart'), default='smart')
    attribute = db.Column(db.Enum('common', 'uncommon'), default='common')
    bind_service_profile_id = db.Column(db.Integer(), default=None)
    bind_RAIO_profile_index = db.Column(db.String(), default='-')
    priority = db.Column(db.String())
    native_vlan = db.Column(db.Integer())

