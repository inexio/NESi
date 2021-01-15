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


class AlcatelPortSchema(PortSchema):
    class Meta:
        model = Port
        fields = PortSchema.Meta.fields + ('shutdown', 'speed', 'noise_margin_up', 'noise_margin_down',
                                           'tgt_noise_margin_up', 'tgt_noise_margin_down', 'attenuation_up',
                                           'attenuation_down', 'attained_upstream', 'attained_downstream',
                                           'threshold_upstream', 'threshold_downstream', 'max_delay_upstream',
                                           'max_delay_downsteam', 'if_index', 'type', 'high_speed', 'connector_present',
                                           'media', 'largest_pkt_size', 'curr_bandwith', 'phy_addr',
                                           'last_chg_opr_stat', 'pkts_unknown_proto', 'in_octets', 'out_octets',
                                           'in_ucast_pkts', 'out_ucast_pkts', 'in_mcast_pkts', 'out_mcast_pkts',
                                           'in_broadcast_pkts', 'out_broadcast_pkts', 'in_discard_pkts',
                                           'out_discard_pkts', 'in_err_pkts', 'out_err_pkts', 'in_octets_hc',
                                           'out_octets_hc', 'in_ucast_pkts_hc', 'out_ucast_pkts_hc',
                                           'in_mcast_pkts_hc', 'out_mcast_pkts_hc', 'in_broadcast_pkts_hc',
                                           'out_broadcast_pkts_hc', 'position', 'diag_avail_status', 'los', 'tx_fault',
                                           'tx_power', 'rx_power', 'tx_bias_current', 'supply_voltage', 'temperature',
                                           'temperature_tca', 'voltage_tca', 'bias_current_tca', 'tx_power_tca',
                                           'rx_power_tca', 'rssi_profile_id', 'rssi_state', 'inp_up', 'inp_dn',
                                           'interl_us', 'interl_dn', 'cur_op_mode', 'rinit_1d', 'actual_tps_tc_mode',
                                           'rtx_mode_up', 'rtx_mode_dn', 'total_reset_attempt', 'success_reset_attempt',
                                           'cur_init_state', 'auto_negotiation', 'mtu', 'service_profile_id',
                                           'spectrum_profile_id', 'vect_profile_id', 'dpbo_profile_id',
                                           'qos_profile_id', 'inventory_status', 'alu_part_num', 'tx_wavelength',
                                           'fiber_type', 'rssi_sfptype', 'mfg_name', 'mfg_oui', 'mfg_date',
                                           'egress_port')
