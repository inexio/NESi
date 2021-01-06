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

from experimental.db_models.config_models import *
from .ont_models import AlcatelOnt
from .cpe_models import AlcatelCpe
from .service_port_models import AlcatelServicePort


@add_portschema
class AlcatelPort(alcatel_base):
    __tablename__ = 'alcatelport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String(), default='')
    onts = relationship('AlcatelOnt', backref='AlcatelPort')
    cpes = relationship('AlcatelCpe', backref='AlcatelPort')
    service_port = relationship('AlcatelServicePort', backref='AlcatelPort')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'), nullable=True)
    card_id = Column(Integer, ForeignKey('alcatelcard.id'))

    # Alcatel data
    type = Column(Enum('pon', 'ethernet-line'), default='pon')
    shutdown = Column(Boolean(), default=False)
    speed = Column(Enum('10M', '1G', '10G'), default='1G')
    operational_state = Column(Enum('down', 'up'), default='down')
    admin_state = Column(Enum('down', 'up'), default='down')
    upstream = Column(Integer(), default=0)
    downstream = Column(Integer(), default=0)
    upstream_max = Column(String(), default="100000")
    downstream_max = Column(String(), default="100000")
    cur_init_state = Column(Enum('up', 'down', 'shutdown'), default='down')
    auto_negotiation = Column(Boolean(), default=True)
    mtu = Column(Integer(), default=1500)
    noise_margin_up = Column(Integer(), default=0)
    noise_margin_down = Column(Integer(), default=0)
    tgt_noise_margin_up = Column(Integer(), default=0)
    tgt_noise_margin_down = Column(Integer(), default=0)
    attenuation_up = Column(Integer(), default=0)
    attenuation_down = Column(Integer(), default=0)
    attained_upstream = Column(Integer(), default=0)
    attained_downstream = Column(Integer(), default=0)
    threshold_upstream = Column(Integer(), default=0)
    threshold_downstream = Column(Integer(), default=0)
    max_delay_upstream = Column(Integer(), default=0)
    max_delay_downsteam = Column(Integer(), default=0)
    if_index = Column(Integer(), default=94502912)
    high_speed = Column(Integer(), default=0)
    connector_present = Column(Enum('not-applicable'), default='not-applicable')
    media = Column(FLOAT, default=0.0)
    largest_pkt_size = Column(Integer(), default=0)
    curr_bandwith = Column(Integer(), default=1244000000)
    phy_addr = Column(String(), default='')
    last_chg_opr_stat = Column(String(), default='352-02:55:19')
    pkts_unknown_proto = Column(Integer(), default=0)
    in_octets = Column(Integer(), default=0)
    out_octets = Column(Integer(), default=0)
    in_ucast_pkts = Column(Integer(), default=0)
    out_ucast_pkts = Column(Integer(), default=0)
    in_mcast_pkts = Column(Integer(), default=0)
    out_mcast_pkts = Column(Integer(), default=0)
    in_broadcast_pkts = Column(Integer(), default=0)
    out_broadcast_pkts = Column(Integer(), default=0)
    in_discard_pkts = Column(Integer(), default=0)
    out_discard_pkts = Column(Integer(), default=0)
    in_err_pkts = Column(Integer(), default=0)
    out_err_pkts = Column(Integer(), default=0)
    in_octets_hc = Column(Integer(), default=0)
    out_octets_hc = Column(Integer(), default=0)
    in_ucast_pkts_hc = Column(Integer(), default=0)
    out_ucast_pkts_hc = Column(Integer(), default=0)
    in_mcast_pkts_hc = Column(Integer(), default=0)
    out_mcast_pkts_hc = Column(Integer(), default=0)
    in_broadcast_pkts_hc = Column(Integer(), default=0)
    out_broadcast_pkts_hc = Column(Integer(), default=0)
    position = Column(String())
    diag_avail_status = Column(Enum('no-error'), default='no-error')
    los = Column(Enum('not-available'), default='not-available')
    tx_fault = Column(Enum('no-tx-fault'), default='no-tx-fault')
    tx_power = Column(String(), default='"3.85 dBm"')
    rx_power = Column(Enum('not-available'), default='not-available')
    tx_bias_current = Column(String(), default='"16.17 mA"')
    supply_voltage = Column(String(), default='"3.23 VDC"')
    temperature = Column(String(), default='"57.39 degrees Celsius"')
    temperature_tca = Column(Enum('normal-value'), default='normal-value')
    voltage_tca = Column(Enum('normal-value'), default='normal-value')
    bias_current_tca = Column(Enum('normal-value'), default='normal-value')
    tx_power_tca = Column(Enum('normal-value'), default='normal-value')
    rx_power_tca = Column(Enum('normal-value'), default='normal-value')
    rssi_profile_id = Column(Integer, default=65535)
    rssi_state = Column(Enum('enable'), default='enable')
    inp_up = Column(Integer(), default=0)
    inp_dn = Column(Integer(), default=0)
    interl_us = Column(Integer(), default=0)
    interl_dn = Column(Integer(), default=0)
    cur_op_mode = Column(Enum('default'), default='default')
    rinit_1d = Column(Integer(), default=0)
    actual_tps_tc_mode = Column(Enum('ptm'), default='ptm')
    rtx_mode_up = Column(Enum('unknown'), default='unknown')
    rtx_mode_dn = Column(Enum('unknown'), default='unknown')
    total_reset_attempt = Column(Integer(), default=0)
    success_reset_attempt = Column(Integer(), default=0)
    service_profile_id = Column(Integer(), default=None, nullable=True)
    spectrum_profile_id = Column(Integer(), default=None, nullable=True)
    vect_profile_id = Column(Integer(), default=None, nullable=True)
    dpbo_profile_id = Column(Integer(), default=None, nullable=True)
    qos_profile_id = Column(Integer(), default=None, nullable=True)
    inventory_status = Column(Enum('cage-empty', 'no-error'), default='cage-empty')
    alu_part_num = Column(String(), default='not-available')
    tx_wavelength = Column(String(), default='not-available')
    fiber_type = Column(Enum('not-available', 'single-mode'), default='not-available')
    rssi_sfptype = Column(String(), default='not-available')
    mfg_name = Column(String(), default='NEOPHOTONICS')
    mfg_oui = Column(String(), default='000000')
    mfg_date = Column(String(), default='27/10/2016')
    egress_port = Column(Boolean(), default=False)
    
    def __repr__(self):
        return "<AlcatelPort(id='%s', name='%s', box_id='%s' and card_id='%s')>" %\
               (self.id, self.name, self.box_id, self.card_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_fields()
        self.set_subcomponents()

    def set_fields(self):
        self.description = "Physical port " + self.name
        self.operational_state = "up"
        self.admin_state = "up"
        self.upstream = 10000
        self.downstream = 25000
        self.upstream_max = "100000"
        self.downstream_max = "100000"

    def set_subcomponents(self):
        service_port = AlcatelServicePort(name=self.name, connected_type='port', box_id=self.box_id)
        self.service_port = [service_port]

        onts = []
        for x in ('/1', '/2', '/3'):
            ont = AlcatelOnt(name=self.name + x, box_id=self.box_id)
            onts.append(ont)
        self.onts = onts

        cpes = []
        for x in ('/1', '/2', '/3'):
            cpe = AlcatelCpe(name=self.name + x, box_id=self.box_id)
            cpes.append(cpe)
        self.cpes = cpes
        return

