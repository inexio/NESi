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

from nesi.devices.softbox.api import db
from ..models.interface_models import Interface


class Channel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    chan_profile_name = db.Column(db.String(), default='')
    curr_rate_u = db.Column(db.String(), default=0)
    curr_rate_d = db.Column(db.String(), default=0)
    prev_rate_u = db.Column(db.String(), default=0)
    prev_rate_d = db.Column(db.String(), default=0)
    curr_delay_u = db.Column(db.String(), default=0)
    curr_delay_d = db.Column(db.String(), default=0)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))
    interfaces = db.relationship('Interface', backref='Channel', lazy='dynamic')
