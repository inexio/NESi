# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst
from ..config_models import *


@add_mgmtportschema
class AlcatelMgmtPort(alcatel_base):
    __tablename__ = 'alcatelmgmtport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String(64))
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    mgmt_card_id = Column(Integer, ForeignKey('alcatelmgmtcard.id'))

    admin_state = Column(Enum('up', 'down'), default='down')
    operational_state = Column(Enum('up', 'down'), default='down')

    def __repr__(self):
        return "<AlcatelMgmtPort(id='%s', name='%s', box_id='%s' and mgmt_card_id='%s')>" % \
               (self.id, self.name, self.box_id, self.mgmt_card_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
