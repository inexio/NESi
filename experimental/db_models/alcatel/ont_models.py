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
from .ontport_models import AlcatelOntPort


@add_ontschema
class AlcatelOnt(alcatel_base):
    __tablename__ = 'alcatelont'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String())
    ont_ports = relationship('AlcatelOntPort', backref='AlcatelOnt')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    port_id = Column(Integer, ForeignKey('alcatelport.id'))

    admin_state = Column(Enum('down', 'up'), default='down')
    operational_state = Column(Enum('down', 'up'), default='down')
    vendor_id = Column(String(), default=None)
    version = Column(String(), default=None)
    index = Column(Integer(), nullable=False, default=1)
    type = Column(Enum('10gbaselr', '1000basebx10u', '100basetxfd', '1000basebx10d', '100basebx10d',
                             '1000baselx10'), default='1000baselx10')
    basebx10d = Column(Enum('yes', 'no'), default='no')
    media_available = Column(Enum('available', 'not-available'), default='not-available')
    jabber_state = Column(Enum('jabber', 'no-jabber'), default='no-jabber')
    b100basefxfd = Column(Enum('yes', 'no'), default='no')
    b100baselx10 = Column(Enum('yes', 'no'), default='no')
    b100basebx10d = Column(Enum('yes', 'no'), default='no')
    b100basebx10u = Column(Enum('yes', 'no'), default='no')
    b100basetxfd = Column(Enum('yes', 'no'), default='no')
    b1000basetfd = Column(Enum('yes', 'no'), default='no')
    b10gbasetfd = Column(Enum('yes', 'no'), default='no')
    b1000basesxfd = Column(Enum('yes', 'no'), default='no')
    b1000baselx10 = Column(Enum('yes', 'no'), default='no')
    b1000baselxfd = Column(Enum('yes', 'no'), default='no')
    b1000basebx10u = Column(Enum('yes', 'no'), default='no')
    b1000basebx10d = Column(Enum('yes', 'no'), default='no')
    b10gbaser = Column(Enum('yes', 'no'), default='no')
    b10gbaselr = Column(Enum('yes', 'no'), default='no')
    b10gbaseer = Column(Enum('yes', 'no'), default='no')
    b2500basex = Column(Enum('yes', 'no'), default='no')
    auto_neg_supported = Column(Boolean(), default=False)
    auto_neg_status = Column(Enum('configuring', 'disabled', 'complete'), default='disabled')
    cap100base_tfd = Column(Enum('yes', 'no'), default='no')
    cap1000base_xfd = Column(Enum('yes', 'no'), default='no')
    cap1000base_tfd = Column(Enum('yes', 'no'), default='no')
    cap10gbase_tfd = Column(Enum('yes', 'no'), default='no')
    act_num_data_ports = Column(Integer(), nullable=True)
    act_num_voice_ports = Column(Integer(), nullable=True)
    actual_card_type = Column(Enum('ethernet', 'pon'), default='ethernet')
    actual_ont_integ = Column(Enum('integrated'))
    actual_serial_num = Column(String(), nullable=False, default='123456789')
    actual_version_num = Column(String(), nullable=False, default='123456789')
    actual_vendorid = Column(String(), nullable=False, default='123456789')
    actual_cardid = Column(String(), nullable=False, default='123456789')
    state = Column(Enum('enabled'))
    provision = Column(Boolean(), default=False)
    sernum = Column(String(), nullable=False, default='123456789')
    subscriber_locid = Column(Enum('DEFAULT', '0000000000'), default='DEFAULT')
    loss_of_signal = Column(Enum('no'), default='no')
    loss_of_ack = Column(Enum('no'), default='no')
    loss_of_gem = Column(Enum('no'), default='no')
    physical_eqpt_err = Column(Enum('no'), default='no')
    startup_failure = Column(Enum('no'), default='no')
    signal_degrade = Column(Enum('no'), default='no')
    ont_disabled = Column(Enum('no'), default='no')
    msg_error_msg = Column(Enum('no'), default='no')
    inactive = Column(Enum('no'), default='no')
    loss_of_frame = Column(Enum('no'), default='no')
    signal_fail = Column(Enum('no'), default='no')
    dying_gasp = Column(Enum('no'), default='no')
    deactivate_fail = Column(Enum('no'), default='no')
    loss_of_ploam = Column(Enum('no'), default='no')
    drift_of_window = Column(Enum('no'), default='no')
    remote_defect_ind = Column(Enum('no'), default='no')
    loss_of_key_sync = Column(Enum('no'), default='no')
    rogue_ont_disabled = Column(Enum('no'), default='no')
    diff_reach = Column(Enum('no'), default='no')
    ont_olt_distance = Column(String(), default='12.4')
    eqpt_ver_num = Column(String(), default='3FE56389AEBA01')
    sw_ver_act = Column(String(), default='3FE56065AFGB89')
    sw_ver_psv = Column(String(), default='3FE56065AFBB48')
    equip_id = Column(String(), default='3FE56389AEBA01')
    actual_num_slots = Column(Integer(), default=1)
    num_tconts = Column(Integer(), default=32)
    num_trf_sched = Column(Integer(), default=32)
    num_prio_queues = Column(Integer(), default=124)
    auto_sw_planned_ver = Column(String(), default='3FE56065AFGB89')
    auto_sw_download_ver = Column(String(), default='3FE56065AFGB89')
    yp_serial_no = Column(String(), default='B1406AF0')
    oper_spec_ver = Column(Enum('unknown'), default='unknown')
    act_ont_type = Column(Enum('sfu'), default='sfu')
    act_txpower_ctrl = Column(Enum('tx-rx'), default='tx-rx')
    sn_bundle_status = Column(Enum('idle'), default='idle')
    cfgfile1_ver_act = Column(String(), default='')
    cfgfile1_ver_psv = Column(String(), default='')
    cfgfile2_ver_act = Column(String(), default='')
    cfgfile2_ver_psv = Column(String(), default='')
    rx_signal_level = Column(Float(), default=-14.788)
    tx_signal_level = Column(Float(), default=2.146)
    ont_temperature = Column(Float(), default=49.602)
    ont_voltage = Column(Float(), default=3.32)
    laser_bias_curr = Column(Float(), default=9950.0)
    olt_rx_sig_level = Column(Float(), default=-18.8)

    def __repr__(self):
        return "<AlcatelOnt(id='%s', name='%s', box_id='%s' and port_id='%s')>" % \
               (self.id, self.name, self.box_id, self.port_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_subcomponents()

    def set_subcomponents(self):
        ont_ports = []
        for x in ('/1', '/2', '/3'):
            port = AlcatelOntPort(name=self.name + x, box_id=self.box_id)
            ont_ports.append(port)
        self.ont_ports = ont_ports
