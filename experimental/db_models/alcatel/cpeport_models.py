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
from .service_port_models import AlcatelServicePort


@add_cpeportschema
class AlcatelCpePort(alcatel_base):
    __tablename__ = 'alcatelcpeport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String())
    service_port = relationship('AlcatelServicePort', backref='AlcatelCpePort')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    cpe_id = Column(Integer, ForeignKey('alcatelcpe.id'))

    def __repr__(self):
        return "<AlcatelCpePorts(id='%s', name='%s', box_id='%s' and description='%s')>" % \
               (self.id, self.name, self.box_id, self.description)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_subcomponents()

    def set_subcomponents(self):
        service_port = AlcatelServicePort(name=self.name, connected_type='cpe', box_id=self.box_id)
        self.service_port = [service_port]
        return

