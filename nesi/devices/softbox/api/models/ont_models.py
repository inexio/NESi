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

from nesi.devices.softbox.api import db
from .ontport_models import OntPort


class Ont(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    admin_state = db.Column(db.Enum('0', '1'), default='0')  # Alcatel: 0 => down, 1 => up; Huawei: 0 => offline, 1 => online
    operational_state = db.Column(db.Enum('0', '1'), default='0')  # Alcatel: 0 => down, 1 => up; Huawei: 0 => offline, 1 => online
    vendor_id = db.Column(db.String(), default=None)
    version = db.Column(db.String(), default=None)

    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    port_id = db.Column(db.Integer, db.ForeignKey('port.id'))
    ont_ports = db.relationship('OntPort', backref='Ont', lazy='dynamic')

    # Alcatel data
    index = db.Column(db.Integer(), nullable=False, default=1)
    type = db.Column(db.Enum('10gbaselr', '1000basebx10u', '100basetxfd', '1000basebx10d', '100basebx10d',
                             '1000baselx10'), default='1000baselx10')
    basebx10d = db.Column(db.Enum('yes', 'no'), default='no')
    media_available = db.Column(db.Enum('available', 'not-available'), default='not-available')
    jabber_state = db.Column(db.Enum('jabber', 'no-jabber'), default='no-jabber')
    b100basefxfd = db.Column(db.Enum('yes', 'no'), default='no')
    b100baselx10 = db.Column(db.Enum('yes', 'no'), default='no')
    b100basebx10d = db.Column(db.Enum('yes', 'no'), default='no')
    b100basebx10u = db.Column(db.Enum('yes', 'no'), default='no')
    b100basetxfd = db.Column(db.Enum('yes', 'no'), default='no')
    b1000basetfd = db.Column(db.Enum('yes', 'no'), default='no')
    b10gbasetfd = db.Column(db.Enum('yes', 'no'), default='no')
    b1000basesxfd = db.Column(db.Enum('yes', 'no'), default='no')
    b1000baselx10 = db.Column(db.Enum('yes', 'no'), default='no')
    b1000baselxfd = db.Column(db.Enum('yes', 'no'), default='no')
    b1000basebx10u = db.Column(db.Enum('yes', 'no'), default='no')
    b1000basebx10d = db.Column(db.Enum('yes', 'no'), default='no')
    b10gbaser = db.Column(db.Enum('yes', 'no'), default='no')
    b10gbaselr = db.Column(db.Enum('yes', 'no'), default='no')
    b10gbaseer = db.Column(db.Enum('yes', 'no'), default='no')
    b2500basex = db.Column(db.Enum('yes', 'no'), default='no')
    auto_neg_supported = db.Column(db.Boolean(), default=False)
    auto_neg_status = db.Column(db.Enum('configuring', 'disabled', 'complete'), default='disabled')
    cap100base_tfd = db.Column(db.Enum('yes', 'no'), default='no')
    cap1000base_xfd = db.Column(db.Enum('yes', 'no'), default='no')
    cap1000base_tfd = db.Column(db.Enum('yes', 'no'), default='no')
    cap10gbase_tfd = db.Column(db.Enum('yes', 'no'), default='no')
    act_num_data_ports = db.Column(db.Integer(), nullable=True)
    act_num_voice_ports = db.Column(db.Integer(), nullable=True)
    actual_card_type = db.Column(db.Enum('ethernet', 'pon'), default='ethernet')
    actual_ont_integ = db.Column(db.Enum('integrated'))
    actual_serial_num = db.Column(db.String(), nullable=False, default='123456789')
    actual_version_num = db.Column(db.String(), nullable=False, default='123456789')
    actual_vendorid = db.Column(db.String(), nullable=False, default='123456789')
    actual_cardid = db.Column(db.String(), nullable=False, default='123456789')
    state = db.Column(db.Enum('enabled'))
    provision = db.Column(db.Boolean(), default=False)
    sernum = db.Column(db.String(), nullable=False, default='123456789')
    subscriber_locid = db.Column(db.Enum('DEFAULT', '0000000000'), default='DEFAULT')
    loss_of_signal = db.Column(db.Enum('no'), default='no')
    loss_of_ack = db.Column(db.Enum('no'), default='no')
    loss_of_gem = db.Column(db.Enum('no'), default='no')
    physical_eqpt_err = db.Column(db.Enum('no'), default='no')
    startup_failure = db.Column(db.Enum('no'), default='no')
    signal_degrade = db.Column(db.Enum('no'), default='no')
    ont_disabled = db.Column(db.Enum('no'), default='no')
    msg_error_msg = db.Column(db.Enum('no'), default='no')
    inactive = db.Column(db.Enum('no'), default='no')
    loss_of_frame = db.Column(db.Enum('no'), default='no')
    signal_fail = db.Column(db.Enum('no'), default='no')
    dying_gasp = db.Column(db.Enum('no'), default='no')
    deactivate_fail = db.Column(db.Enum('no'), default='no')
    loss_of_ploam = db.Column(db.Enum('no'), default='no')
    drift_of_window = db.Column(db.Enum('no'), default='no')
    remote_defect_ind = db.Column(db.Enum('no'), default='no')
    loss_of_key_sync = db.Column(db.Enum('no'), default='no')
    rogue_ont_disabled = db.Column(db.Enum('no'), default='no')
    diff_reach = db.Column(db.Enum('no'), default='no')
    ont_olt_distance = db.Column(db.String(), default='12.4')
    eqpt_ver_num = db.Column(db.String(), default='3FE56389AEBA01')
    sw_ver_act = db.Column(db.String(), default='3FE56065AFGB89')
    sw_ver_psv = db.Column(db.String(), default='3FE56065AFBB48')
    equip_id = db.Column(db.String(), default='3FE56389AEBA01')
    actual_num_slots = db.Column(db.Integer(), default=1)
    num_tconts = db.Column(db.Integer(), default=32)
    num_trf_sched = db.Column(db.Integer(), default=32)
    num_prio_queues = db.Column(db.Integer(), default=124)
    auto_sw_planned_ver = db.Column(db.String(), default='3FE56065AFGB89')
    auto_sw_download_ver = db.Column(db.String(), default='3FE56065AFGB89')
    yp_serial_no = db.Column(db.String(), default='B1406AF0')
    oper_spec_ver = db.Column(db.Enum('unknown'), default='unknown')
    act_ont_type = db.Column(db.Enum('sfu'), default='sfu')
    act_txpower_ctrl = db.Column(db.Enum('tx-rx'), default='tx-rx')
    sn_bundle_status = db.Column(db.Enum('idle'), default='idle')
    cfgfile1_ver_act = db.Column(db.String(), default='')
    cfgfile1_ver_psv = db.Column(db.String(), default='')
    cfgfile2_ver_act = db.Column(db.String(), default='')
    cfgfile2_ver_psv = db.Column(db.String(), default='')
    rx_signal_level = db.Column(db.Float(), default=-14.788)
    tx_signal_level = db.Column(db.Float(), default=2.146)
    ont_temperature = db.Column(db.Float(), default=49.602)
    ont_voltage = db.Column(db.Float(), default=3.32)
    laser_bias_curr = db.Column(db.Float(), default=9950.0)
    olt_rx_sig_level = db.Column(db.Float(), default=-18.8)

    # Huawei data
    serial_number = db.Column(db.String(), default='485754433AD3209C')
    control_flag = db.Column(db.Enum('active'), default='active')
    config_state = db.Column(db.Enum('normal'), default='normal')
    match_state = db.Column(db.Enum('match'), default='match')
    protect_side = db.Column(db.Enum('no', 'yes'), default='no')
    dba_type = db.Column(db.String(), default='SR')
    ont_distance = db.Column(db.Integer(), default=2000)
    ont_last_distance = db.Column(db.Integer(), default=2000)
    ont_battery_state = db.Column(db.String(), default='not support')
    memory_occupation = db.Column(db.String())
    cpu_occupation = db.Column(db.String())
    temperature = db.Column(db.String(), default='50(C)')
    authentic_type = db.Column(db.String(), default='SN-auth')
    management_mode = db.Column(db.String(), default='OMCI')
    software_work_mode = db.Column(db.String(), default='normal')
    isolation_state = db.Column(db.String(), default='normal')
    ont_ip_zero_address_mask = db.Column(db.String(), default='-')
    last_down_cause = db.Column(db.String(), default='-')
    last_up_time = db.Column(db.String(), default='2020-01-01 00:00:00+01:00')
    last_down_time = db.Column(db.String(), default='-')
    last_dying_gasp = db.Column(db.String(), default='-')
    ont_online_duration = db.Column(db.String())
    type_c_support = db.Column(db.String(), default='Not support')
    interoperability_mode = db.Column(db.String(), default='ITU-T')
    power_reduction_status = db.Column(db.String(), default='-')
    fec_upstream_state = db.Column(db.String(), default='use-profile-config')

    port_number_pots = db.Column(db.Enum('adaptive', '0'), default='adaptive')
    max_adaptive_num_pots = db.Column(db.String, default='32')
    port_number_eth = db.Column(db.Enum('adaptive', '0'), default='adaptive')
    max_adaptive_num_eth = db.Column(db.String(), default='8')
    port_number_vdsl = db.Column(db.Enum('adaptive', '0'), default='0')
    max_adaptive_num_vdsl = db.Column(db.String(), default='-')
    lineprofile_id = db.Column(db.Integer(), nullable=True)
    srvprofile_id = db.Column(db.Integer(), nullable=True)
    software_version = db.Column(db.String(), default=None)

    # PBN data
    mac_address = db.Column(db.String(), default=None)

