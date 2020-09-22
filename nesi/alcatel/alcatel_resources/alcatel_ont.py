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

from nesi.softbox.base_resources.ont import OntCollection, Ont
from nesi.softbox.base_resources import base


class AlcatelOnt(Ont):
    """Represent physical shelf resource."""

    index = base.Field('index')
    type = base.Field('type')
    basebx10d = base.Field('basebx10d')
    media_available = base.Field('media_available')
    jabber_state = base.Field('jabber_state')
    b100basefxfd = base.Field('b100basefxfd')
    b100baselx10 = base.Field('b100baselx10')
    b100basebx10d = base.Field('b100basebx10d')
    b100basebx10u = base.Field('b100basebx10u')
    b100basetxfd = base.Field('b100basetxfd')
    b1000basetfd = base.Field('b1000basetfd')
    b10gbasetfd = base.Field('b10gbasetfd')
    b1000basesxfd = base.Field('b1000basesxfd')
    b1000baselx10 = base.Field('b1000baselx10')
    b1000baselxfd = base.Field('b1000baselxfd')
    b1000basebx10u = base.Field('b1000basebx10u')
    b1000basebx10d = base.Field('b1000basebx10d')
    b10gbaser = base.Field('b10gbaser')
    b10gbaselr = base.Field('b10gbaselr')
    b10gbaseer = base.Field('b10gbaseer')
    b2500basex = base.Field('b2500basex')
    auto_neg_supported = base.Field('auto_neg_supported')
    auto_neg_status = base.Field('auto_neg_status')
    cap100base_tfd = base.Field('cap100base_tfd')
    cap1000base_xfd = base.Field('cap1000base_xfd')
    cap1000base_tfd = base.Field('cap1000base_tfd')
    cap10gbase_tfd = base.Field('cap10gbase_tfd')
    act_num_data_ports = base.Field('act_num_data_ports')
    act_num_voice_ports = base.Field('act_num_voice_ports')
    actual_card_type = base.Field('actual_card_type')
    actual_ont_integ = base.Field('actual_ont_integ')
    actual_serial_num = base.Field('actual_serial_num')
    actual_version_num = base.Field('actual_version_num')
    actual_vendorid = base.Field('actual_vendorid')
    actual_cardid = base.Field('actual_cardid')
    state = base.Field('state')
    provision = base.Field('provision')
    sernum = base.Field('sernum')
    subscriber_locid = base.Field('subscriber_locid')
    loss_of_signal = base.Field('loss_of_signal')
    loss_of_ack = base.Field('loss_of_ack')
    loss_of_gem = base.Field('loss_of_gem')
    physical_eqpt_err = base.Field('physical_eqpt_err')
    startup_failure = base.Field('startup_failure')
    signal_degrade = base.Field('signal_degrade')
    ont_disabled = base.Field('ont_disabled')
    msg_error_msg = base.Field('msg_error_msg')
    inactive = base.Field('inactive')
    loss_of_frame = base.Field('loss_of_frame')
    signal_fail = base.Field('signal_fail')
    dying_gasp = base.Field('dying_gasp')
    deactivate_fail = base.Field('deactivate_fail')
    loss_of_ploam = base.Field('loss_of_ploam')
    drift_of_window = base.Field('drift_of_window')
    remote_defect_ind = base.Field('remote_defect_ind')
    loss_of_key_sync = base.Field('loss_of_key_sync')
    rogue_ont_disabled = base.Field('rogue_ont_disabled')
    diff_reach = base.Field('diff_reach')
    ont_olt_distance = base.Field('ont_olt_distance')
    eqpt_ver_num = base.Field('eqpt_ver_num')
    sw_ver_act = base.Field('sw_ver_act')
    sw_ver_psv = base.Field('sw_ver_psv')
    vendor_id = base.Field('vendor_id')
    equip_id = base.Field('equip_id')
    actual_num_slots = base.Field('actual_num_slots')
    version_number = base.Field('version_number')
    num_tconts = base.Field('num_tconts')
    num_trf_sched = base.Field('num_trf_sched')
    num_prio_queues = base.Field('num_prio_queues')
    auto_sw_planned_ver = base.Field('auto_sw_planned_ver')
    auto_sw_download_ver = base.Field('auto_sw_download_ver')
    yp_serial_no = base.Field('yp_serial_no')
    oper_spec_ver = base.Field('oper_spec_ver')
    act_ont_type = base.Field('act_ont_type')
    act_txpower_ctrl = base.Field('act_txpower_ctrl')
    sn_bundle_status = base.Field('sn_bundle_status')
    cfgfile1_ver_act = base.Field('cfgfile1_ver_act')
    cfgfile1_ver_psv = base.Field('cfgfile1_ver_psv')
    cfgfile2_ver_act = base.Field('cfgfile2_ver_act')
    cfgfile2_ver_psv = base.Field('cfgfile2_ver_psv')

    rx_signal_level = base.Field('rx_signal_level')
    tx_signal_level = base.Field('tx_signal_level')
    ont_temperature = base.Field('ont_temperature')
    ont_voltage = base.Field('ont_voltage')
    laser_bias_curr = base.Field('laser_bias_curr')
    olt_rx_sig_level = base.Field('olt_rx_sig_level')

    def power_up(self):
        """Change ont admin state to up."""
        self.update(admin_state='1')
        self.update(operational_state='1')

    def power_down(self):
        """Change ont admin state to down."""
        self.update(admin_state='0')
        self.update(operational_state='0')

    def set_type(self, type):
        """Change ont type."""
        self.update(type=type)

    def autonegotiate(self):
        """Enable autonegotiating on ont."""
        self.update(auto_neg_supported=True)
        self.update(auto_neg_status='complete')

    def set_cap1000base_xfd(self, value):
        """Set a certain property to the given value."""
        self.update(cap1000base_xfd=value)

    def admin_up(self):
        """Change ont admin state to up."""
        self.update(admin_state='1')

    def admin_down(self):
        """Change ont admin state to down."""
        self.update(admin_state='0')


class AlcatelOntCollection(OntCollection):
    """Represent a collection of ONTs."""

    @property
    def _resource_type(self):
        return AlcatelOnt
