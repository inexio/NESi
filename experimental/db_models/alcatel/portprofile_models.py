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

from experimental.db_models.config_models import *


class AlcatelPortProfile(alcatel_base):
    __tablename__ = 'alcatelportprofile'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String())
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))

    # Alcatel Data
    type = Column(Enum('service', 'spectrum', 'dpbo', 'rtx', 'vect', 'sos', 'ghs', 'qos', 'policer', 'vce',
                             'data-rate', 'noise-margin', 'inp-delay', 'mode-specific-psd'))
    up_policer = Column(String(), default=None, nullable=True)
    down_policer = Column(String(), default=None, nullable=True)
    committed_info_rate = Column(Integer(), default=0, nullable=False)
    committed_burst_size = Column(Integer(), default=0, nullable=False)
    logical_flow_type = Column(Enum('generic'), default='generic')

    def __repr__(self):
        return "<AlcatelPortProfile(id='%s', name='%s'and box_id='%s')>" % \
               (self.id, self.name, self.box_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

