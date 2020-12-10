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


class AlcatelUser(alcatel_base):
    __tablename__ = 'alcatelusers'
    id = Column(Integer(), primary_key=True)
    name = Column(String(), default='user')
    box_id = Column(Integer(), ForeignKey('alcatelbox.id'))
    credentials_id = Column(Integer(), ForeignKey('alcatelcredentials.id'))

    level = Column(Enum('Super', 'Admin', 'Operator', 'User'), default='User')
    status = Column(Enum('Online', 'Offline'), default='Offline')
    profile = Column(Enum('root', 'admin', 'operator', 'commonuser'), default='commonuser')
    append_info = Column(String(), default='-----')
    reenter_num = Column(Integer(), default=3)
    reenter_num_temp = Column(Integer(), default=3)
    lock_status = Column(Enum('Locked', 'Unlocked'), default='Unlocked')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<AlcatelUser(id='%s', name='%s', box_id='%s')>" %\
               (self.id, self.name, self.box_id)
