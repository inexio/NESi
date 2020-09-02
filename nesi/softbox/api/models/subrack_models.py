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
from .card_models import Card


class Subrack(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), default='test')
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    cards = db.relationship('Card', backref='Subrack', lazy='dynamic')
    # data
    description = db.Column(db.String(), default='')
    planned_type = db.Column(db.Enum('rvxs-a', 'not-planned', 'planned', 'nfxs-f'), default='not-planned')
    actual_type = db.Column(db.Enum('rvxs-a', 'not-planned', 'planned', 'nfxs-f'), default='not-planned')
    admin_state = db.Column(db.Enum('unlock', 'lock'), default='unlock')
    operational_state = db.Column(db.Enum('enabled', 'disabled'), default='disabled')
    err_state = db.Column(db.Enum('no-error', 'error'), default='no-error')
    availability = db.Column(db.Enum('available', 'unavailable', 'not-installed'), default='not-installed')
    mode = db.Column(db.Enum('no-extended-lt-slots', 'extended-lt-slots'), default='extended-lt-slots')
    subrack_class = db.Column(db.Enum('main-ethernet', 'main-copper'), default='main-copper')
    serial_no = db.Column(db.String(), default='NOT_AVAILABLE')
    variant = db.Column(db.String(), default='NOT_AVAILABLE')
    ics = db.Column(db.String(), default='NOT_AVAILABLE')

    #huawei
    frame_status = db.Column(db.Enum('active', 'inactive'), default='active')
    temperature = db.Column(db.String(), default='51C')
