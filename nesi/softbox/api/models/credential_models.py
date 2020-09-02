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


class Credential(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    protocol = db.Column(
        db.Enum('password'), nullable=False, default='password')
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(32), nullable=True)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
