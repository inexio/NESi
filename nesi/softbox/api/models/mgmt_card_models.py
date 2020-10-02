# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst
import uuid

from nesi.softbox.api import db
from .mgmt_port_models import MgmtPort


class MgmtCard(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    description = db.Column(db.String(), default='None')
    subrack_id = db.Column(db.Integer, db.ForeignKey('subrack.id'))
    admin_state = db.Column(db.Enum('0', '1'), default='0')
    operational_state = db.Column(db.Enum('0', '1'), default='0')
    mgmt_ports = db.relationship('MgmtPort', backref='MgmtCard', lazy='dynamic')
