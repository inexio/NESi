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

from nesi.softbox.api import db
from ..models.cpeport_models import CpePort


class Cpe(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'), nullable=True)
    ont_port_id = db.Column(db.Integer, db.ForeignKey('ont_port.id'), nullable=True)
    cpe_ports = db.relationship('CpePort', backref='Cpe', lazy='dynamic')
    name = db.Column(db.String(64))
    serial_no = db.Column(db.String(), default='ABCD123456EF')
    admin_state = db.Column(db.Enum('0', '1'), default='0')  # 0 => down, 1 => up
    description = db.Column(db.String())
    mac = db.Column(db.String(64), nullable=False)

    # Huawei specific data fields
    g_994_1_vendor_id = db.Column(db.String(), default='0xB5004946544E590C')
    g_994_1_country_code = db.Column(db.String(), default='0xB500')
    g_994_1_provider_code = db.Column(db.String(), default='IFTN')
    g_994_1_vendor_info = db.Column(db.String(), default='0x590C')
    system_vendor_id = db.Column(db.String(), default='0x040041564D000000')
    system_country_code = db.Column(db.String(), default='0x0400')
    system_provider_code = db.Column(db.String(), default='AVM')
    system_vendor_info = db.Column(db.String(), default='0x0000')
    version_number = db.Column(db.String(), default='1.180.129.93 AB')
    version_number_oct = db.Column(db.String(), default='0x312E3138302E3132392E393320414200')
    vendor_serial_number = db.Column(db.String(), default='444E6DCD4770 F!Box7530 164.07.14')
    self_test_result = db.Column(db.Enum('PASS'), default='PASS')       # find corresponding value(s)
