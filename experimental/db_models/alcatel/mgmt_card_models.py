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
from .mgmt_port_models import AlcatelMgmtPort


class AlcatelMgmtCard(alcatel_base):
    __tablename__ = 'alcatelmgmtcard'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String(), default='')
    mgmt_ports = relationship('AlcatelMgmtPort', backref='AlcatelMgmtCard')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    subrack_id = Column(Integer, ForeignKey('alcatelsubrack.id'))
    
    admin_state = Column(Enum('down', 'up'), default='down')
    operational_state = Column(Enum('down', 'up'), default='down')
    board_name = Column(String(), default='')
    supplier_build_state = Column(Enum('R1G', 'R1D', 'R2B', 'R2A', 'R1K', 'R1H', 'R2B', 'R1E', 'R3D', 'R1C', 'R1A', ''),
                                  default='')
    board_id = Column(Enum('345', '332', '303', '308', '377', '356', '305', '307', '330', '0'), default='0')
    hardware_key = Column(Integer(), default=0)
    software = Column(String(), default='')
    software_name = Column(String(), default='')
    software_revision = Column(String(), default='')
    state = Column(Enum('Ok', 'Empty'), default='Empty')
    serial_number = Column(String(), default='')
    manufacturer_name = Column(String(), default='')
    model_name = Column(String(), default='')
    short_text = Column(String(), default='')
    manufacturer_id = Column(String(), default='')
    manufacturer_part_number = Column(String(), default='')
    manufacturer_build_state = Column(String(), default='')
    customer_id = Column(String(), default='')
    customer_product_id = Column(String(), default='')
    boot_loader = Column(String(), default='')
    processor = Column(String(), default='')
    product = Column(Enum('mgmt'), nullable=False, default='mgmt')

    def __repr__(self):
        return "<AlcatelMgmtCard(id='%s', name='%s', box_id='%s' and subrack_id='%s')>" % \
               (self.id, self.name, self.box_id, self.subrack_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_subcomponents()

    def set_subcomponents(self):
        mgmt_ports = []
        for x in ('/1', '/2', '/3'):
            port = AlcatelMgmtPort(name=self.name + x, box_id=self.box_id, mgmt_card_id=self.id)
            mgmt_ports.append(port)
        self.mgmt_ports = mgmt_ports