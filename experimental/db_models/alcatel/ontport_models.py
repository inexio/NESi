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

from experimental.db_models.base_models import *


class AlcatelOntPort(alcatel_base):
    __tablename__ = 'alcatelontport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String())
    cpes = relationship('AlcatelCpe', backref='AlcatelOntPort')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    ont_id = Column(Integer, ForeignKey('alcatelont.id'))

    operational_state = Column(Enum('down', 'up'), default='down')
    admin_state = Column(Enum('down', 'up'), default='down')
    uni_idx = Column(String(64))
    config_indicator = Column(String(), default='100baset-fd')
    link_status = Column(Enum('up', 'down'), default='up')
    speed = Column(String(), default='1000')

