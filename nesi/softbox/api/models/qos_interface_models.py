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


class QosInterface(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    scheduler_node = db.Column(db.String(64), default='NGLT_Default')
    cac_profile = db.Column(db.String(64), default=None)
    ds_num_rem_queue = db.Column(db.String(64), default='not-applicable')
    us_num_queue = db.Column(db.String(64), default='not-applicable')
    oper_weight = db.Column(db.Integer, default=0)
    oper_rate = db.Column(db.Integer, default=0)
    mc_scheduler_node = db.Column(db.String(64), default=None)
    bc_scheduler_node = db.Column(db.String(64), default=None)
    ds_schedule_tag = db.Column(db.String(64), default='cvlanpbitbased')
    upstream_queue = db.Column(db.Integer, default=0)
    upstream_queue_bandwidth_profile = db.Column(db.String(64), default=None)
    upstream_queue_bandwidth_sharing = db.Column(db.Enum('uni-sharing'), default='uni-sharing')
    upstream_queue_priority = db.Column(db.Integer, default=0)
    upstream_queue_weight = db.Column(db.Integer, default=0)
