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


class PortProfile(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    type = db.Column(db.Enum('service', 'spectrum', 'dpbo', 'rtx', 'vect', 'sos', 'ghs', 'qos', 'policer', 'vce'))
    up_policer = db.Column(db.String(), default=None, nullable=True)
    down_policer = db.Column(db.String(), default=None, nullable=True)
    committed_info_rate = db.Column(db.Integer(), default=0, nullable=False)
    committed_burst_size = db.Column(db.Integer(), default=0, nullable=False)
    logical_flow_type = db.Column(db.Enum('generic'), default='generic')
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
