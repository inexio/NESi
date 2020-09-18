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

from nesi.softbox.base_resources.port_profile import PortProfile, PortProfileCollection, base, logging

LOG = logging.getLogger(__name__)


class HuaweiPortProfile(PortProfile):
    """Represent a PortProfile resource."""

    maximum_bit_error_ratio = base.Field('maximum_bit_error_ratio')
    path_mode = base.Field('path_mode')
    rate = base.Field('rate')
    etr_max = base.Field('etr_max')
    etr_min = base.Field('etr_min')
    ndr_max = base.Field('ndr_max')
    working_mode = base.Field('working_mode')
    eside_electrical_length = base.Field('eside_electrical_length')
    assumed_exchange_psd = base.Field('assumed_exchange_psd')
    eside_cable_model = base.Field('eside_cable_model')
    min_usable_signal = base.Field('min_usable_signal')
    span_frequency = base.Field('span_frequency')
    dpbo_calculation = base.Field('dpbo_calculation')
    snr_margin = base.Field('snr_margin')
    rate_adapt = base.Field('rate_adapt')
    snr_mode = base.Field('snr_mode')
    inp_4khz = base.Field('inp_4khz')
    inp_8khz = base.Field('inp_8khz')
    interleaved_delay = base.Field('interleaved_delay')
    delay_variation = base.Field('delay_variation')
    channel_policy = base.Field('channel_policy')
    nominal_transmit_PSD_ds = base.Field('nominal_transmit_PSD_ds')
    nominal_transmit_PSD_us = base.Field('nominal_transmit_PSD_us')
    aggregate_transmit_power_ds = base.Field('aggregate_transmit_power_ds')
    aggregate_transmit_power_us = base.Field('aggregate_transmit_power_us')
    aggregate_receive_power_us = base.Field('aggregate_receive_power_us')
    upstream_psd_mask_selection = base.Field('upstream_psd_mask_selection')
    psd_class_mask = base.Field('psd_class_mask')
    psd_limit_mask = base.Field('psd_limit_mask')

    l0_time = base.Field('l0_time')
    l2_time = base.Field('l2_time')
    l3_time = base.Field('l3_time')
    max_transmite_power_reduction = base.Field('max_transmite_power_reduction')
    total_max_power_reduction = base.Field('total_max_power_reduction')
    bit_swap_ds = base.Field('bit_swap_ds')
    bit_swap_us = base.Field('bit_swap_us')
    overhead_datarate_us = base.Field('overhead_datarate_us')
    overhead_datarate_ds = base.Field('overhead_datarate_ds')
    allow_transitions_to_idle = base.Field('allow_transitions_to_idle')
    allow_transitions_to_lowpower = base.Field('allow_transitions_to_lowpower')
    reference_clock = base.Field('reference_clock')
    cyclic_extension_flag = base.Field('cyclic_extension_flag')
    force_inp_ds = base.Field('force_inp_ds')
    force_inp_us = base.Field('force_inp_us')
    g_993_2_profile = base.Field('g_993_2_profile')
    mode_specific = base.Field('mode_specific')
    transmode = base.Field('transmode')
    T1_413 = base.Field('T1_413')
    G_992_1 = base.Field('G_992_1')
    G_992_2 = base.Field('G_992_1')
    G_992_3 = base.Field('G_992_3')
    G_992_4 = base.Field('G_992_4')
    G_992_5 = base.Field('G_992_5')
    AnnexB_G_993_2 = base.Field('AnnexB_G_993_2')
    ETSI = base.Field('ETSI')
    us0_psd_mask = base.Field('us0_psd_mask')
    vdsltoneblackout = base.Field('vdsltoneblackout')
    internal_id = base.Field('internal_id')

    vmac_ipoe = base.Field('vmac_ipoe')
    vmac_pppoe = base.Field('vmac_pppoe')
    vmac_pppoa = base.Field('vmac_pppoa')
    vlan_mac = base.Field('vlan_mac')
    packet_policy_multicast = base.Field('packet_policy_multicast')
    packet_policy_unicast = base.Field('packet_policy_unicast')
    security_anti_ipspoofing = base.Field('security_anti_ipspoofing')
    security_anti_macspoofing = base.Field('security_anti_macspoofing')
    igmp_mismatch = base.Field('igmp_mismatch')
    commit = base.Field('commit')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class HuaweiPortProfileCollection(PortProfileCollection):
    """Represent the collection of PortProfiles."""

    @property
    def _resource_type(self):
        return HuaweiPortProfile
