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

from experimental.db_models.config_models import *


class AlcatelRoute(alcatel_base):
    __tablename__ = 'alcatelroute'
    id = Column(Integer(), primary_key=True)
    dst = Column(String(23))
    gw = Column(String(23))
    metric = Column(Integer(), default=1)
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    sub_mask = Column(Integer(), default=None)


