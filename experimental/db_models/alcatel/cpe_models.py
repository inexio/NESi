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

from .cpeport_models import AlcatelCpePort


class AlcatelCpe(alcatel_base):
    __tablename__ = 'alcatelcpe'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String())
    cpe_ports = relationship('AlcatelCpePort', backref='AlcatelCpe')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    port_id = Column(Integer, ForeignKey('alcatelport.id'), nullable=True)
    ont_port_id = Column(Integer, ForeignKey('alcatelontport.id'), nullable=True)

    serial_no = Column(String(), default='ABCD123456EF')
    admin_state = Column(Enum('down', 'up'), default='down')
    mac = Column(String(64), nullable=False)
