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


class Route(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dst = db.Column(db.String(23))
    gw = db.Column(db.String(23))
    metric = db.Column(db.Integer(), default=1)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))

    sub_mask = db.Column(db.Integer(), default=None)


