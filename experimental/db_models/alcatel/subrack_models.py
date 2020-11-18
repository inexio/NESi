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

from ..base_models import *
from .card_models import AlcatelCard
from .mgmt_card_models import AlcatelMgmtCard


class AlcatelSubrack(alcatel_base):
    __tablename__ = 'alcatelsubrack'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64), default='test')
    description = Column(String(), default='')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    cards = relationship('AlcatelCard', backref='AlcatelSubrack')
    mgmt_cards = relationship('AlcatelMgmtCard', backref='AlcatelSubrack')
    
    # data
    planned_type = Column(Enum('rvxs-a', 'not-planned', 'planned', 'nfxs-f'), default='not-planned')
    actual_type = Column(Enum('rvxs-a', 'not-planned', 'planned', 'nfxs-f'), default='not-planned')
    admin_state = Column(Enum('lock', 'unlock'), default='lock')
    operational_state = Column(Enum('disabled', 'enabled'), default='disabled')
    err_state = Column(Enum('no-error', 'error'), default='no-error')
    availability = Column(Enum('available', 'unavailable', 'not-installed'), default='not-installed')
    mode = Column(Enum('no-extended-lt-slots', 'extended-lt-slots'), default='extended-lt-slots')
    subrack_class = Column(Enum('main-ethernet', 'main-copper'), default='main-copper')
    serial_no = Column(String(), default='NOT_AVAILABLE')
    variant = Column(String(), default='NOT_AVAILABLE')
    ics = Column(String(), default='NOT_AVAILABLE')
