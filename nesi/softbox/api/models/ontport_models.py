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


class OntPort(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    operational_state = db.Column(db.Enum('0', '1'), default='0')  # Alcatel: 0 => down, 1 => up; Huawei: 0 => offline, 1 => online
    admin_state = db.Column(db.Enum('0', '1', '2'), default='0')  # Alcatel: 0 => down, 1 => up, 2 => not-appl; Huawei: 0 => offline, 1 => online
    # pon
    uni_idx = db.Column(db.String(64))
    config_indicator = db.Column(db.String(), default='100baset-fd')
    link_status = db.Column(db.Enum('up', 'down'), default='up')

    speed = db.Column(db.String(), default='1000')
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    ont_id = db.Column(db.Integer, db.ForeignKey('ont.id'))
    cpes = db.relationship('Cpe', backref='OntPort', lazy='dynamic')

    # Huawei data
    ont_port_index = db.Column(db.Integer())
    ont_port_type = db.Column(db.Enum('GE', 'ETH', 'POTS', 'VDSL', 'TDM', 'MOCA', 'CATV'), default='GE')
    duplex = db.Column(db.Enum('full', 'auto_full', 'auto'), default='full')
    link_state = db.Column(db.Enum('up', 'down'), default='down')
    ring_status = db.Column(db.String(), default='-')

    qinq_mode = db.Column(db.Enum('unconcern'), default='unconcern')
    priority_policy = db.Column(db.Enum('unconcern'), default='unconcern')
    inbound = db.Column(db.Enum('unconcern'), default='unconcern')
    outbound = db.Column(db.Enum('unconcern'), default='unconcern')
    downstream_mode = db.Column(db.Enum('operation'), default='operation')
    mismatch_policy = db.Column(db.Enum('discard'), default='discard')
    dscp_mapping_table_index = db.Column(db.Integer(), default=0)
    service_type = db.Column(db.String())
    service_index = db.Column(db.Integer())
    s_vlan = db.Column(db.Integer())
    s_pri = db.Column(db.String())
    c_vlan = db.Column(db.Integer())
    c_pri = db.Column(db.String())
    encap = db.Column(db.String())
    s_pri_policy = db.Column(db.String())
    igmp_mode = db.Column(db.String(), default='-')
    igmp_vlan = db.Column(db.String(), default='-')
    igmp_pri = db.Column(db.String(), default='-')
    max_mac_count = db.Column(db.String(), default='-')

    vlan_id = db.Column(db.Integer, db.ForeignKey('vlan.id'))
