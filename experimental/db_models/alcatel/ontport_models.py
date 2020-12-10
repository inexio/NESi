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
from .cpe_models import AlcatelCpe


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

    def __repr__(self):
        return "<AlcatelOntPort(id='%s', name='%s', box_id='%s' and ont_id='%s')>" % \
               (self.id, self.name, self.box_id, self.ont_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_subcomponents()

    def set_subcomponents(self):
        cpes = []
        for x in ('/1', '/2', '/3'):
            port = AlcatelCpe(name=self.name + x, box_id=self.box_id)
            cpes.append(port)
        self.cpes = cpes
