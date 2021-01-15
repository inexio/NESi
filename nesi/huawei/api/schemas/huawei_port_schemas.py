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

from nesi.softbox.api.schemas.port_schemas import *


class HuaweiPortSchema(PortSchema):
    class Meta:
        model = Port
        fields = PortSchema.Meta.fields + ('line_template', 'loopback', 'sos_profile', 'sos_profile_num',
                                           'alarm_template', 'dynamic_profile_index', 'dynamic_profile_name',
                                           'hardware', 'last_up_time', 'last_down_time', 'show_time',
                                           'nte_power_status', 'current_operational_mode', 'cpes', 'description',
                                           'total_count_of_line_training', 'result_last_initialization',
                                           'total_bytes_us', 'total_packets_us', 'total_bytes_ds', 'total_packets_ds',
                                           'total_discarded_packets_ds', 'channel_packets_discarded_ds',
                                           'dynamic_profile', 'alarm_template_num', 'line_spectrum_profile',
                                           'spectrum_profile_num', 'upbo_profile', 'upbo_profile_num', 'dpbo_profile',
                                           'dpbo_profile_num', 'rfi_profile', 'rfi_profile_num',
                                           'noise_margin_profile', 'noise_margin_profile_num',
                                           'virtual_noise_profile', 'virtual_noise_profile_num', 'inm_profile',
                                           'inm_profile_num', 'line_template_num', 'standard_port_in_training',
                                           'channel_ds_data_rate_profile', 'channel_ds_data_rate_profile_num',
                                           'channel_us_data_rate_profile', 'channel_us_data_rate_profile_num',
                                           'channel_inp_delay_profile', 'channel_inp_data_rate_profile_num',
                                           'channel_ds_rate_adapt_ratio', 'channel_us_rate_adapt_ratio',
                                           'current_power_management_state', 'retransmission_used_us',
                                           'retransmission_used_ds', 'signal_attenuation_ds_1',
                                           'signal_attenuation_us_1', 'line_attenuation_ds_1',
                                           'line_attenuation_us_1', 'act_line_rate_ds_1', 'act_line_rate_us_1',
                                           'line_snr_margin_ds_1', 'line_snr_margin_us_1', 'vdsl_2_psd_class_mask',
                                           'act_psd_ds', 'act_psd_us', 'act_klo_co', 'act_klo_cpe',
                                           'us_1_band_act_klo_val', 'us_2_band_act_klo_val', 'us_3_band_act_klo_val',
                                           'us_4_band_act_klo_val', 'ds_1_band_act_klo_val', 'ds_2_band_act_klo_val',
                                           'ds_3_band_act_klo_val', 'ds_4_band_act_klo_val',
                                           'receive_signal_threshhold_ds', 'receive_signal_threshhold_us',
                                           'total_output_power_ds', 'total_output_power_us', 'current_vdsl_2_profile',
                                           'coding_gain_ds', 'coding_gain_us', 'power_cut_back_ds',
                                           'signal_attenuation_ds_2', 'line_attenuation_ds_2', 'line_snr_margin_ds_2',
                                           'signal_attenuation_us_2', 'line_attenuation_us_2', 'line_snr_margin_us_2',
                                           'signal_attenuation_ds_3', 'line_attenuation_ds_3', 'line_snr_margin_ds_3',
                                           'actual_limit_psd_mask', 'actual_transmit_rate_adapt_ds',
                                           'actual_transmit_rate_adapt_us', 'actual_inp_of_roc_ds',
                                           'actual_inp_of_roc_us', 'actual_snr_margin_of_roc_ds',
                                           'actual_snr_margin_of_roc_us', 'trellis_mode_ds', 'trellis_mode_us',
                                           'last_down_cause', 'port_energy_saving_flag', 'xpon_mac_chipset_state',
                                           'signal_detect', 'available_bandwidth', 'illegal_rogue_ont',
                                           'optical_module_status', 'laser_state', 'tx_fault_h', 'temperature_h',
                                           'tx_bias_current_h', 'supply_voltage_h', 'tx_power_h', 'vendor_name',
                                           'vendor_rev', 'vendor_oui', 'vendor_pn', 'vendor_sn', 'date_code',
                                           'vendor_specific', 'module_type', 'module_sub_type', 'used_type',
                                           'encapsulation_time', 'sff_8472_compliance', 'max_distance', 'max_rate',
                                           'rate_identifier', 'wave_length', 'fiber_type_h', 'identifier',
                                           'ext_identifier', 'connector', 'encoding', 'length_9_um', 'length_50_um',
                                           'length_62_5_um', 'length_copper', 'length_50_um_om_3', 'br_max', 'br_min',
                                           'cc_base', 'cc_exit', 'rx_power_warning_threshold',
                                           'rx_power_alarm_threshold', 'tx_power_warning_threshold',
                                           'tx_power_alarm_threshold', 'tx_bias_warning_threshold',
                                           'tx_bias_alarm_threshold', 'supply_voltage_warning_threshold',
                                           'supply_voltage_alarm_threshold', 'temperature_warning_threshold',
                                           'temperature_alarm_threshold', 'min_distance', 'native_vlan', 'mdi',
                                           'speed_h', 'duplex', 'flow_ctrl', 'active_state', 'link', 'detecting_time',
                                           'tx_state', 'resume_detect', 'detect_interval', 'resume_duration',
                                           'auto_sensing', 'alm_prof_15_min', 'warn_prof_15_min', 'alm_prof_24_hour',
                                           'warn_prof_24_hour', 'optic_status', 'combo_status', 'temperature_h_exact',
                                           'supply_voltage_h_exact', 'tx_bias_current_h_exact', 'tx_power_h_exact',
                                           'rx_power_h_exact', 'vlan_id', 'rx_power_h', 'vectoring_group',
                                           'vectoring_profile_id', 'template_name', 'ont_autofind')
