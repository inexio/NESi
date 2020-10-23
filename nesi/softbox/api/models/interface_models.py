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

from nesi.softbox.api import db


class Interface(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    chan_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))
    logport_id = db.Column(db.Integer, db.ForeignKey('log_port.id'))

    # vcc
    vcc_profile = db.Column(db.String(), default='')  # default or profile_name, default:= vpi=0 and vci=33
    vlan_profile = db.Column(db.String(), default='')  # default or profile_name, must be untagged
    number_of_conn_services = db.Column(db.Integer(), default=0)
    reconfiguration_allowed = db.Column(db.Enum('true', 'false'), default='true')
    services_connected = db.Column(db.String(), default='')
