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


class PortProfile(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String())
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    type = db.Column(db.Enum('service', 'spectrum', 'dpbo', 'rtx', 'vect', 'sos', 'ghs', 'qos', 'policer', 'vce',
                             'data-rate', 'noise-margin', 'inp-delay', 'mode-specific-psd'))

    # Alcatel Data
    up_policer = db.Column(db.String(), default=None, nullable=True)
    down_policer = db.Column(db.String(), default=None, nullable=True)
    committed_info_rate = db.Column(db.Integer(), default=0, nullable=False)
    committed_burst_size = db.Column(db.Integer(), default=0, nullable=False)
    logical_flow_type = db.Column(db.Enum('generic'), default='generic')

    # Huawei data
    maximum_bit_error_ratio = db.Column(db.Integer(), default=None)
    path_mode = db.Column(db.Integer(), default=None)
    rate = db.Column(db.String(), default=None)
    etr_max = db.Column(db.Integer(), default=None)
    etr_min = db.Column(db.Integer(), default=None)
    ndr_max = db.Column(db.Integer(), default=None)
    working_mode = db.Column(db.Integer(), default=None)
    eside_electrical_length = db.Column(db.String(), default=None)
    assumed_exchange_psd = db.Column(db.String(), default=None)
    eside_cable_model = db.Column(db.String(), default=None)
    min_usable_signal = db.Column(db.Integer(), default=None)
    span_frequency = db.Column(db.String(), default=None)
    dpbo_calculation = db.Column(db.Integer(), default=None)
    snr_margin = db.Column(db.String(), default=None)
    rate_adapt = db.Column(db.String(), default=None)
    snr_mode = db.Column(db.String(), default=None)
    inp_4khz = db.Column(db.String(), default=None)
    inp_8khz = db.Column(db.String(), default=None)
    interleaved_delay = db.Column(db.String(), default=None)
    delay_variation = db.Column(db.Integer(), default=None)
    channel_policy = db.Column(db.Integer(), default=None)
    nominal_transmit_PSD_ds = db.Column(db.Integer(), default=None)
    nominal_transmit_PSD_us = db.Column(db.Integer(), default=None)
    aggregate_transmit_power_ds = db.Column(db.Integer(), default=None)
    aggregate_transmit_power_us = db.Column(db.Integer(), default=None)
    aggregate_receive_power_us = db.Column(db.Integer(), default=None)
    upstream_psd_mask_selection = db.Column(db.Integer(), default=None)
    psd_class_mask = db.Column(db.Integer(), default=None)
    psd_limit_mask = db.Column(db.Integer(), default=None)
    l0_time = db.Column(db.Integer(), default=None)
    l2_time = db.Column(db.Integer(), default=None)
    l3_time = db.Column(db.Integer(), default=None)
    max_transmite_power_reduction = db.Column(db.Integer(), default=None)
    total_max_power_reduction = db.Column(db.Integer(), default=None)
    bit_swap_ds = db.Column(db.Integer(), default=None)
    bit_swap_us = db.Column(db.Integer(), default=None)
    overhead_datarate_us = db.Column(db.Integer(), default=None)
    overhead_datarate_ds = db.Column(db.Integer(), default=None)
    allow_transitions_to_idle = db.Column(db.Integer(), default=None)
    allow_transitions_to_lowpower = db.Column(db.Integer(), default=None)
    reference_clock = db.Column(db.String(), default=None)
    cyclic_extension_flag = db.Column(db.Integer(), default=None)
    force_inp_ds = db.Column(db.Integer(), default=None)
    force_inp_us = db.Column(db.Integer(), default=None)
    g_993_2_profile = db.Column(db.Integer(), default=None)
    mode_specific = db.Column(db.String(), default=None)
    transmode = db.Column(db.String(), default=None)
    T1_413 = db.Column(db.String(), default=None)
    G_992_1 = db.Column(db.String(), default=None)
    G_992_2 = db.Column(db.String(), default=None)
    G_992_3 = db.Column(db.String(), default=None)
    G_992_4 = db.Column(db.String(), default=None)
    G_992_5 = db.Column(db.String(), default=None)
    AnnexB_G_993_2 = db.Column(db.String(), default=None)
    ETSI = db.Column(db.String(), default=None)
    us0_psd_mask = db.Column(db.Integer(), default=None)
    vdsltoneblackout = db.Column(db.String(), default=None)
    internal_id = db.Column(db.Integer(), default=None)

    vmac_ipoe = db.Column(db.Enum('enable', 'disable'), default=None)
    vmac_pppoe = db.Column(db.Enum('enable', 'disable'), default=None)
    vmac_pppoa = db.Column(db.Enum('enable', 'disable'), default=None)
    vlan_mac = db.Column(db.Enum('forwarding', 'discard'), default=None)
    packet_policy_multicast = db.Column(db.Enum('forward', 'discard'), default=None)
    packet_policy_unicast = db.Column(db.Enum('forward', 'discard'), default=None)
    security_anti_ipspoofing = db.Column(db.Enum('enable', 'disable'), default=None)
    security_anti_macspoofing = db.Column(db.Enum('enable', 'disable'), default=None)
    igmp_mismatch = db.Column(db.Enum('transparent'), default=None)
    commit = db.Column(db.Boolean(), default=False)
    number = db.Column(db.Integer, default=None)
