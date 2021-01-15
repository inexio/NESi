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

from nesi.softbox.base_resources.port import Port, PortCollection, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiPort(Port):
    """Represent physical port resource."""

    cpes = base.Field('cpes')
    description = base.Field('description')
    loopback = base.Field('loopback')
    line_template = base.Field('line_template')
    alarm_template = base.Field('alarm_template')
    dynamic_profile_index = base.Field('dynamic_profile_index')
    dynamic_profile_name = base.Field('dynamic_profile_name')
    hardware = base.Field('hardware')
    last_up_time = base.Field('last_up_time')
    last_down_time = base.Field('last_down_time')
    show_time = base.Field('show_time')
    nte_power_status = base.Field('nte_power_status')
    current_operational_mode = base.Field('current_operational_mode')
    total_count_of_line_training = base.Field('total_count_of_line_training')
    result_last_initialization = base.Field('result_last_initialization')
    total_bytes_us = base.Field('total_bytes_us')
    total_packets_us = base.Field('total_packets_us')
    total_bytes_ds = base.Field('total_bytes_ds')
    total_packets_ds = base.Field('total_packets_ds')
    total_discarded_packets_ds = base.Field('total_discarded_packets_ds')
    channel_packets_discarded_ds = base.Field('channel_packets_discarded_ds')

    dynamic_profile = base.Field('dynamic_profile')
    line_template_num = base.Field('line_template_num')
    alarm_template_num = base.Field('alarm_template_num')
    line_spectrum_profile = base.Field('line_spectrum_profile')
    spectrum_profile_num = base.Field('spectrum_profile_num')
    upbo_profile = base.Field('upbo_profile')
    upbo_profile_num = base.Field('upbo_profile_num')
    dpbo_profile = base.Field('dpbo_profile')
    dpbo_profile_num = base.Field('dpbo_profile_num')
    rfi_profile = base.Field('rfi_profile')
    rfi_profile_num = base.Field('rfi_profile_num')
    noise_margin_profile = base.Field('noise_margin_profile')
    noise_margin_profile_num = base.Field('noise_margin_profile_num')
    virtual_noise_profile = base.Field('virtual_noise_profile')
    virtual_noise_profile_num = base.Field('virtual_noise_profile_num')
    inm_profile = base.Field('inm_profile')
    inm_profile_num = base.Field('inm_profile_num')
    sos_profile = base.Field('sos_profile')
    sos_profile_num = base.Field('sos_profile_num')
    channel_ds_data_rate_profile = base.Field('channel_ds_data_rate_profile')
    channel_ds_data_rate_profile_num = base.Field('channel_ds_data_rate_profile_num')
    channel_us_data_rate_profile = base.Field('channel_us_data_rate_profile')
    channel_us_data_rate_profile_num = base.Field('channel_us_data_rate_profile_num')
    channel_inp_delay_profile = base.Field('channel_inp_delay_profile')
    channel_inp_data_rate_profile_num = base.Field('channel_inp_data_rate_profile_num')
    channel_ds_rate_adapt_ratio = base.Field('channel_ds_rate_adapt_ratio')
    channel_us_rate_adapt_ratio = base.Field('channel_us_rate_adapt_ratio')
    standard_port_in_training = base.Field('standard_port_in_training')
    current_power_management_state = base.Field('current_power_management_state')
    retransmission_used_us = base.Field('retransmission_used_us')
    retransmission_used_ds = base.Field('retransmission_used_ds')
    signal_attenuation_ds_1 = base.Field('signal_attenuation_ds_1')
    signal_attenuation_us_1 = base.Field('signal_attenuation_us_1')
    line_attenuation_ds_1 = base.Field('line_attenuation_ds_1')
    line_attenuation_us_1 = base.Field('line_attenuation_us_1')
    act_line_rate_ds_1 = base.Field('act_line_rate_ds_1')
    act_line_rate_us_1 = base.Field('act_line_rate_us_1')
    line_snr_margin_ds_1 = base.Field('line_snr_margin_ds_1')
    line_snr_margin_us_1 = base.Field('line_snr_margin_us_1')
    vdsl_2_psd_class_mask = base.Field('vdsl_2_psd_class_mask')
    act_psd_ds = base.Field('act_psd_ds')
    act_psd_us = base.Field('act_psd_us')
    act_klo_co = base.Field('act_klo_co')
    act_klo_cpe = base.Field('act_klo_cpe')
    us_1_band_act_klo_val = base.Field('us_1_band_act_klo_val')
    us_2_band_act_klo_val = base.Field('us_2_band_act_klo_val')
    us_3_band_act_klo_val = base.Field('us_3_band_act_klo_val')
    us_4_band_act_klo_val = base.Field('us_4_band_act_klo_val')
    ds_1_band_act_klo_val = base.Field('ds_1_band_act_klo_val')
    ds_2_band_act_klo_val = base.Field('ds_2_band_act_klo_val')
    ds_3_band_act_klo_val = base.Field('ds_3_band_act_klo_val')
    ds_4_band_act_klo_val = base.Field('ds_4_band_act_klo_val')
    receive_signal_threshhold_ds = base.Field('receive_signal_threshhold_ds')
    receive_signal_threshhold_us = base.Field('receive_signal_threshhold_us')
    total_output_power_ds = base.Field('total_output_power_ds')
    total_output_power_us = base.Field('total_output_power_us')
    current_vdsl_2_profile = base.Field('current_vdsl_2_profile')
    coding_gain_ds = base.Field('coding_gain_ds')
    coding_gain_us = base.Field('coding_gain_us')
    power_cut_back_ds = base.Field('power_cut_back_ds')
    signal_attenuation_ds_2 = base.Field('signal_attenuation_ds_2')
    line_attenuation_ds_2 = base.Field('line_attenuation_ds_2')
    line_snr_margin_ds_2 = base.Field('line_snr_margin_ds_2')
    signal_attenuation_us_2 = base.Field('signal_attenuation_us_2')
    line_attenuation_us_2 = base.Field('line_attenuation_us_2')
    line_snr_margin_us_2 = base.Field('line_snr_margin_us_2')
    signal_attenuation_ds_3 = base.Field('signal_attenuation_ds_3')
    line_attenuation_ds_3 = base.Field('line_attenuation_ds_3')
    line_snr_margin_ds_3 = base.Field('line_snr_margin_ds_3')
    actual_limit_psd_mask = base.Field('actual_limit_psd_mask')
    actual_transmit_rate_adapt_ds = base.Field('actual_transmit_rate_adapt_ds')
    actual_transmit_rate_adapt_us = base.Field('actual_transmit_rate_adapt_us')
    actual_inp_of_roc_ds = base.Field('actual_inp_of_roc_ds')
    actual_inp_of_roc_us = base.Field('actual_inp_of_roc_us')
    actual_snr_margin_of_roc_ds = base.Field('actual_snr_margin_of_roc_ds')
    actual_snr_margin_of_roc_us = base.Field('actual_snr_margin_of_roc_us')
    trellis_mode_ds = base.Field('trellis_mode_ds')
    trellis_mode_us = base.Field('trellis_mode_us')
    last_down_cause = base.Field('last_down_cause')
    port_energy_saving_flag = base.Field('port_energy_saving_flag')
    xpon_mac_chipset_state = base.Field('xpon_mac_chipset_state')
    signal_detect = base.Field('signal_detect')
    available_bandwidth = base.Field('available_bandwidth')
    illegal_rogue_ont = base.Field('illegal_rogue_ont')
    optical_module_status = base.Field('optical_module_status')
    laser_state = base.Field('laser_state')
    tx_fault_h = base.Field('tx_fault_h')
    temperature_h = base.Field('temperature_h')
    tx_bias_current_h = base.Field('tx_bias_current_h')
    supply_voltage_h = base.Field('supply_voltage_h')
    tx_power_h = base.Field('tx_power_h')
    vendor_name = base.Field('vendor_name')
    vendor_rev = base.Field('vendor_rev')
    vendor_oui = base.Field('vendor_oui')
    vendor_pn = base.Field('vendor_pn')
    vendor_sn = base.Field('vendor_sn')
    date_code = base.Field('date_code')
    vendor_specific = base.Field('vendor_specific')
    module_type = base.Field('module_type')
    module_sub_type = base.Field('module_sub_type')
    used_type = base.Field('used_type')
    encapsulation_time = base.Field('encapsulation_time')
    sff_8472_compliance = base.Field('sff_8472_compliance')
    min_distance = base.Field('min_distance')
    max_distance = base.Field('max_distance')
    max_rate = base.Field('max_rate')
    rate_identifier = base.Field('rate_identifier')
    wave_length = base.Field('wave_length')
    fiber_type_h = base.Field('fiber_type_h')
    identifier = base.Field('identifier')
    ext_identifier = base.Field('ext_identifier')
    connector = base.Field('connector')
    encoding = base.Field('encoding')
    length_9_um = base.Field('length_9_um')
    length_50_um = base.Field('length_50_um')
    length_62_5_um = base.Field('length_62_5_um')
    length_copper = base.Field('length_copper')
    length_50_um_om_3 = base.Field('length_50_um_om_3')
    br_max = base.Field('br_max')
    br_min = base.Field('br_min')
    cc_base = base.Field('cc_base')
    cc_exit = base.Field('cc_exit')
    rx_power_warning_threshold = base.Field('rx_power_warning_threshold')
    rx_power_alarm_threshold = base.Field('rx_power_alarm_threshold')
    tx_power_warning_threshold = base.Field('tx_power_warning_threshold')
    tx_power_alarm_threshold = base.Field('tx_power_alarm_threshold')
    tx_bias_warning_threshold = base.Field('tx_bias_warning_threshold')
    tx_bias_alarm_threshold = base.Field('tx_bias_alarm_threshold')
    supply_voltage_warning_threshold = base.Field('supply_voltage_warning_threshold')
    supply_voltage_alarm_threshold = base.Field('supply_voltage_alarm_threshold')
    temperature_warning_threshold = base.Field('temperature_warning_threshold')
    temperature_alarm_threshold = base.Field('temperature_alarm_threshold')
    optic_status = base.Field('optic_status')
    native_vlan = base.Field('native_vlan')
    mdi = base.Field('mdi')
    speed_h = base.Field('speed_h')
    duplex = base.Field('duplex')
    flow_ctrl = base.Field('flow_ctrl')
    active_state = base.Field('active_state')
    link = base.Field('link')
    detecting_time = base.Field('detecting_time')
    tx_state = base.Field('tx_state')
    resume_detect = base.Field('resume_detect')
    detect_interval = base.Field('detect_interval')
    resume_duration = base.Field('resume_duration')
    auto_sensing = base.Field('auto_sensing')
    alm_prof_15_min = base.Field('alm_prof_15_min')
    warn_prof_15_min = base.Field('warn_prof_15_min')
    alm_prof_24_hour = base.Field('alm_prof_24_hour')
    warn_prof_24_hour = base.Field('warn_prof_24_hour')
    combo_status = base.Field('combo_status')

    temperature_h_exact = base.Field('temperature_h_exact')
    supply_voltage_h_exact = base.Field('supply_voltage_h_exact')
    tx_bias_current_h_exact = base.Field('tx_bias_current_h_exact')
    tx_power_h_exact = base.Field('tx_power_h_exact')
    rx_power_h_exact = base.Field('rx_power_h_exact')
    rx_power_h = base.Field('rx_power_h')
    vlan_id = base.Field('vlan_id')
    vectoring_group = base.Field('vectoring_group')
    vectoring_profile_id = base.Field('vectoring_profile_id')
    ont_autofind = base.Field('ont_autofind')
    template_name = base.Field('template_name')

    def admin_up(self):
        self.update(admin_state='2')

    def admin_down(self):
        self.update(admin_state='0')

    def port_downstream_set(self, ds_rate):
        self.update(downstream_max=ds_rate)

    def port_upstream_set(self, us_rate):
        self.update(upstream_max=us_rate)

    def set_vlan_id(self, id):
        self.update(vlan_id=id)

    def set_vectoring_group(self, group):
        self.update(vectoring_group=group)

    def enable_ont_autofind(self):
        self.update(ont_autofind=True)

    def disable_ont_autofind(self):
        self.update(ont_autofind=False)

    def set_template_name(self, template):
        self.update(template_name=template)

    def set_vectoring_profile_id(self, id):
        self.update(vectoring_profile_id=id)

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class HuaweiPortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return HuaweiPort
