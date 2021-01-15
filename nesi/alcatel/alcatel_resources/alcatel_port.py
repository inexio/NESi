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

from nesi.softbox.base_resources.port import PortCollection, Port, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelPort(Port):
    """Represent physical port resource."""

    mode = base.Field('mode')
    shutdown = base.Field('shutdown')
    speed = base.Field('speed')
    noise_margin_up = base.Field('noise_margin_up')
    noise_margin_down = base.Field('noise_margin_down')
    tgt_noise_margin_up = base.Field('tgt_noise_margin_up')
    tgt_noise_margin_down = base.Field('tgt_noise_margin_down')
    attenuation_up = base.Field('attenuation_up')
    attenuation_down = base.Field('attenuation_down')
    attained_upstream = base.Field('attenuation_down')
    attained_downstream = base.Field('attained_downstream')
    threshold_upstream = base.Field('threshold_upstream')
    threshold_downstream = base.Field('threshold_downstream')
    max_delay_upstream = base.Field('max_delay_upstream')
    max_delay_downsteam = base.Field('max_delay_downsteam')
    if_index = base.Field('if_index')
    type = base.Field('type')
    high_speed = base.Field('high_speed')
    connector_present = base.Field('connector_present')
    media = base.Field('media')
    largest_pkt_size = base.Field('largest_pkt_size')
    curr_bandwith = base.Field('curr_bandwith')
    phy_addr = base.Field('phy_addr')
    last_chg_opr_stat = base.Field('last_chg_opr_stat')
    pkts_unknown_proto = base.Field('pkts_unknown_proto')
    in_octets = base.Field('in_octets')
    out_octets = base.Field('out_octets')
    in_ucast_pkts = base.Field('in_ucast_pkts')
    out_ucast_pkts = base.Field('out_ucast_pkts')
    in_mcast_pkts = base.Field('in_mcast_pkts')
    out_mcast_pkts = base.Field('out_mcast_pkts')
    in_broadcast_pkts = base.Field('in_broadcast_pkts')
    out_broadcast_pkts = base.Field('out_broadcast_pkts')
    in_discard_pkts = base.Field('in_discard_pkts')
    out_discard_pkts = base.Field('out_discard_pkts')
    in_err_pkts = base.Field('in_err_pkts')
    out_err_pkts = base.Field('out_err_pkts')
    in_octets_hc = base.Field('in_octets_hc')
    out_octets_hc = base.Field('out_octets_hc')
    in_ucast_pkts_hc = base.Field('in_ucast_pkts_hc')
    out_ucast_pkts_hc = base.Field('out_ucast_pkts_hc')
    in_mcast_pkts_hc = base.Field('in_mcast_pkts_hc')
    out_mcast_pkts_hc = base.Field('out_mcast_pkts_hc')
    in_broadcast_pkts_hc = base.Field('in_broadcast_pkts_hc')
    out_broadcast_pkts_hc = base.Field('out_broadcast_pkts_hc')
    position = base.Field('position')
    diag_avail_status = base.Field('diag_avail_status')
    los = base.Field('los')
    tx_fault = base.Field('tx_fault')
    tx_power = base.Field('tx_power')
    rx_power = base.Field('rx_power')
    tx_bias_current = base.Field('tx_bias_current')
    supply_voltage = base.Field('supply_voltage')
    temperature = base.Field('temperature')
    temperature_tca = base.Field('temperature_tca')
    voltage_tca = base.Field('voltage_tca')
    bias_current_tca = base.Field('bias_current_tca')
    tx_power_tca = base.Field('tx_power_tca')
    rx_power_tca = base.Field('rx_power_tca')
    rssi_profile_id = base.Field('rssi_profile_id')
    rssi_state = base.Field('rssi_state')
    inp_up = base.Field('inp_up')
    inp_dn = base.Field('inp_dn')
    interl_us = base.Field('interl_us')
    interl_dn = base.Field('interl_dn')
    cur_op_mode = base.Field('cur_op_mode')
    rinit_1d = base.Field('rinit_1d')
    actual_tps_tc_mode = base.Field('actual_tps_tc_mode')
    rtx_mode_up = base.Field('rtx_mode_up')
    rtx_mode_dn = base.Field('rtx_mode_dn')
    total_reset_attempt = base.Field('total_reset_attempt')
    success_reset_attempt = base.Field('success_reset_attempt')
    cur_init_state = base.Field('cur_init_state')
    auto_negotiation = base.Field('auto_negotiation')
    mtu = base.Field('mtu')
    service_profile_id = base.Field('service_profile_id')
    spectrum_profile_id = base.Field('spectrum_profile_id')
    vect_profile_id = base.Field('vect_profile_id')
    dpbo_profile_id = base.Field('dpbo_profile_id')
    inventory_status = base.Field('inventory_status')
    alu_part_num = base.Field('alu_part_num')
    tx_wavelength = base.Field('tx_wavelength')
    fiber_type = base.Field('fiber_type')
    rssi_sfptype = base.Field('rssi_sfptype')
    mfg_name = base.Field('mfg_name')
    mfg_oui = base.Field('mfg_oui')
    mfg_date = base.Field('mfg_date')
    egress_port = base.Field('egress_port')

    def update_profile(self, port_profile_id, profile_type):
        """Set the profile_id for the specific profile_type"""
        if profile_type == 'service':
            self.update(service_profile_id=port_profile_id)
        elif profile_type == 'spectrum':
            self.update(spectrum_profile_id=port_profile_id)
        elif profile_type == 'vect':
            self.update(vect_profile_id=port_profile_id)
        elif profile_type == 'dpbo':
            self.update(dpbo_profile_id=port_profile_id)

    def set_description(self, user):
        """Set the user of the port"""
        self.update(description=user)

    def set_egress_port(self, bool):
        """Set the user of the port"""
        self.update(egress_port=bool)


class AlcatelPortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return AlcatelPort
