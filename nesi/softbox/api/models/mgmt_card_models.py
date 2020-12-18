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
import uuid

from nesi.softbox.api import db
from .mgmt_port_models import MgmtPort


class MgmtCard(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    subrack_id = db.Column(db.Integer, db.ForeignKey('subrack.id'))
    mgmt_ports = db.relationship('MgmtPort', backref='MgmtCard', lazy='dynamic')

    description = db.Column(db.String(), default='')
    admin_state = db.Column(db.Enum('0', '1'), default='0')
    operational_state = db.Column(db.Enum('0', '1'), default='0')
    board_name = db.Column(db.String(), default='')
    supplier_build_state = db.Column(db.Enum('R1G', 'R1D', 'R2B', 'R2A', 'R1K', 'R1H', 'R2B', 'R1E', 'R3D', 'R1C',
                                             'R1A', ''), default='')
    board_id = db.Column(db.Enum('345', '332', '303', '308', '377', '356', '305', '307', '330', '0'), default='0')
    hardware_key = db.Column(db.Integer(), default=0)
    software = db.Column(db.String(), default='')
    software_name = db.Column(db.String(), default='')
    software_revision = db.Column(db.String(), default='')
    state = db.Column(db.Enum('Ok', 'Empty'), default='Empty')
    serial_number = db.Column(db.String(), default='')
    manufacturer_name = db.Column(db.String(), default='')
    model_name = db.Column(db.String(), default='')
    short_text = db.Column(db.String(), default='')
    manufacturer_id = db.Column(db.String(), default='')
    manufacturer_part_number = db.Column(db.String(), default='')
    manufacturer_build_state = db.Column(db.String(), default='')
    customer_id = db.Column(db.String(), default='')
    customer_product_id = db.Column(db.String(), default='')
    boot_loader = db.Column(db.String(), default='')
    processor = db.Column(db.String(), default='')
    product = db.Column(db.Enum('mgmt'), nullable=False, default='mgmt')
