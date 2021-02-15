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

from nesi.devices.softbox.api import db


class VlanInterface(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    vlan_id = db.Column(db.Integer, db.ForeignKey('vlan.id'))
    admin_state = db.Column(db.Enum('0', '1'), default='0') # 0 => DOWN, 1 => UP
    line_proto_state = db.Column(db.Enum('0', '1'), default='0')  # 0 => DOWN, 1 => UP
    input_packets = db.Column(db.Integer(), default=0)
    input_bytes = db.Column(db.Integer(), default=0)
    input_multicasts = db.Column(db.Integer(), default=0)
    output_packets = db.Column(db.Integer(), default=0)
    output_bytes = db.Column(db.Integer(), default=0)
    output_multicasts = db.Column(db.Integer(), default=0)
    internet_protocol = db.Column(db.Enum('enabled', 'disabled'), default='disabled')
    internet_address = db.Column(db.String(), default=None, nullable=True)
    subnet_num = db.Column(db.String(), default=None, nullable=True)
    broadcast_address = db.Column(db.String(), default='0.0.0.0')
    sending_frames_format = db.Column(db.String(), default='PKTFMT_ETHNT_2')
    hardware_address = db.Column(db.String(), default='384c-4f1e-c1cc')
    mtu = db.Column(db.Integer(), default=1500)
