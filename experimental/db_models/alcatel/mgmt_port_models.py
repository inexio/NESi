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


class AlcatelMgmtPort(alcatel_base):
    __tablename__ = 'alcatelmgmtport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String(64))
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    mgmt_card_id = Column(Integer, ForeignKey('alcatelmgmtcard.id'))

    admin_state = Column(Enum('0', '1'), default='0')
    operational_state = Column(Enum('0', '1'), default='0')
