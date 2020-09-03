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

from nesi.softbox.api.schemas.ont_schemas import *


class AlcatelOntSchema(OntSchema):
    class Meta:
        model = Ont
        fields = OntSchema.Meta.fields + ('index', 'type', 'basebx10d', 'media_available', 'jabber_state',
                                          'b100basefxfd', 'b100baselx10', 'b100basebx10d', 'b100basebx10u',
                                          'b100basetxfd', 'b1000basetfd', 'b10gbasetfd', 'b1000basesxfd',
                                          'b1000baselx10', 'b1000baselxfd', 'b1000basebx10u', 'b1000basebx10d',
                                          'b10gbaser', 'b10gbaselr', 'b10gbaseer', 'b2500basex', 'auto_neg_supported',
                                          'auto_neg_status', 'cap100base_tfd', 'cap1000base_xfd', 'cap1000base_tfd',
                                          'cap10gbase_tfd', 'act_num_data_ports', 'act_num_voice_ports',
                                          'actual_card_type', 'actual_ont_integ', 'actual_serial_num',
                                          'actual_version_num', 'actual_vendorid', 'actual_cardid', 'state',
                                          'provision', 'sernum', 'subscriber_locid', 'loss_of_signal', 'loss_of_ack',
                                          'loss_of_gem', 'physical_eqpt_err', 'startup_failure', 'signal_degrade',
                                          'ont_disabled', 'msg_error_msg', 'inactive', 'loss_of_frame', 'signal_fail',
                                          'dying_gasp', 'deactivate_fail', 'loss_of_ploam', 'drift_of_window',
                                          'remote_defect_ind', 'loss_of_key_sync', 'rogue_ont_disabled', 'diff_reach',
                                          'ont_olt_distance', 'eqpt_ver_num', 'sw_ver_act', 'sw_ver_psv', 'vendor_id',
                                          'equip_id', 'actual_num_slots', 'version_number', 'num_tconts',
                                          'num_trf_sched', 'num_prio_queues', 'auto_sw_planned_ver',
                                          'auto_sw_download_ver', 'yp_serial_no', 'oper_spec_ver', 'act_ont_type',
                                          'act_txpower_ctrl', 'sn_bundle_status', 'cfgfile1_ver_act',
                                          'cfgfile1_ver_psv', 'cfgfile2_ver_act', 'cfgfile2_ver_psv', 'rx_signal_level',
                                          'tx_signal_level', 'ont_temperature', 'ont_voltage', 'laser_bias_curr',
                                          'olt_rx_sig_level')
