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

from nesi.softbox.api.schemas.portprofile_schemas import *


class HuaweiPortProfileSchema(PortProfileSchema):
    class Meta:
        model = PortProfile
        fields = PortProfileSchema.Meta.fields + ('maximum_bit_error_ratio', 'path_mode', 'rate', 'etr_max', 'etr_min',
                                                  'ndr_max', 'working_mode', 'eside_electrical_length',
                                                  'assumed_exchange_psd', 'eside_cable_model', 'min_usable_signal',
                                                  'span_frequency', 'dpbo_calculation', 'snr_margin', 'rate_adapt',
                                                  'snr_mode', 'inp_4khz', 'inp_8khz', 'interleaved_delay',
                                                  'delay_variation', 'channel_policy', 'nominal_transmit_PSD_ds',
                                                  'nominal_transmit_PSD_us', 'aggregate_transmit_power_ds',
                                                  'aggregate_transmit_power_us', 'aggregate_receive_power_us',
                                                  'upstream_psd_mask_selection', 'psd_class_mask', 'psd_limit_mask',
                                                  'l0_time', 'l2_time', 'l3_time', 'max_transmite_power_reduction',
                                                  'total_max_power_reduction', 'bit_swap_ds', 'bit_swap_us',
                                                  'overhead_datarate_us', 'overhead_datarate_ds',
                                                  'allow_transitions_to_idle', 'allow_transitions_to_lowpower',
                                                  'reference_clock', 'cyclic_extension_flag', 'force_inp_ds',
                                                  'force_inp_us', 'g_993_2_profile', 'mode_specific', 'transmode',
                                                  'T1_413', 'G_992_1', 'G_992_2', 'G_992_3', 'G_992_4', 'G_992_5',
                                                  'AnnexB_G_993_2', 'ETSI', 'us0_psd_mask', 'vdsltoneblackout',
                                                  'vmac_ipoe', 'vmac_pppoe', 'vmac_pppoa',
                                                  'vlan_mac', 'packet_policy_multicast', 'packet_policy_unicast',
                                                  'security_anti_ipspoofing', 'security_anti_macspoofing',
                                                  'igmp_mismatch', 'commit', 'internal_id')
