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

from ..models.interface_models import Interface
from nesi.devices.softbox.api import db


class LogPort(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    ports = db.Column(db.String(), default='')
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    interfaces = db.relationship('Interface', backref='LogPort', lazy='dynamic')
    label1 = db.Column(db.String(), default='""')
    label2 = db.Column(db.String(), default='""')
    description = db.Column(db.String(), default='""')
    operational_state = db.Column(db.Enum('0', '1'), default='0')
    admin_state = db.Column(db.Enum('0', '1'), default='0')
    profile = db.Column(db.String(), default='default')
