# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from experimental.db_models.config_models import *
from .port_models import AlcatelPort


class AlcatelCard(alcatel_base):
    __tablename__ = 'alcatelcard'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    description = Column(String(), default='""')

    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    subrack_id = Column(Integer, ForeignKey('alcatelsubrack.id'))
    ports = relationship('AlcatelPort', backref='AlcatelCard')

    # Alcatel specific data
    ppc = Column(Enum('8', '16', '32', '48', '64'), default='32')
    product = Column(Enum('xdsl', 'vdsl', 'adsl', 'sdsl', 'ftth-pon', 'ftth', 'mgnt', 'analog', 'isdn'),
                        nullable=False, default='vdsl')
    position = Column(String())
    entry_vlan_number = Column(Integer())
    planned_type = Column(Enum('rdlt-c', 'rant-a', 'nant-a', 'nrnt-a', 'fant-f', 'relt-a', 'nelt-b', 'fglt-b',
                                     'ngfc-f', 'empty'), default='empty')
    dual_tag_mode = Column(Boolean(), default=False)
    actual_type = Column(Enum('rdlt-c', 'rant-a', 'nant-a', 'nrnt-a', 'fant-f', 'relt-a', 'nelt-b', 'fglt-b',
                                    'ngfc-f', 'empty'), default='empty')
    admin_state = Column(Enum('disabled', 'unlock'), default='disabled')
    operational_state = Column(Enum('disabled', 'enabled'), default='disabled')
    err_state = Column(Enum('no-error', 'error', 'type-mismatch'), default='no-error')
    availability = Column(Enum('available', 'unavailable', 'not-installed'), default='available')
    alarm_profile = Column(Enum('none'), default='none')
    capab_profile = Column(Enum('32port_xDSL', 'fttu_lt', 'not_applicable'), default='32port_xDSL')
    manufacturer = Column(Enum('ALCL', ''), default='')
    mnemonic = Column(Enum('RDLT-C', 'FGLT-B', 'FANT-F', 'NGFC-F', 'RANT-A', 'NANT-A', 'NRNT-A', 'RELT-A',
                                 'NELT-B', 'NGFC-F', ''), default='')
    pba_code = Column(String(), default='')
    fpba_code = Column(String(), default='')
    fpba_ics = Column(String(), default='')
    clei_code = Column(String(), default='')
    serial_no = Column(String(), default='')
    failed_test = Column(String(), default='00:00:00:00')
    lt_restart_time = Column(String(), default='1970-01-01:00:00:00')
    lt_restart_cause = Column(Enum('poweron', 'poweroff', 'other'), default='poweron')
    lt_restart_num = Column(Integer(), default=0)
    mgnt_entity_oamipaddr = Column(String(), default='0.0.0.0')
    mgnt_entity_pairnum = Column(Integer(), default=0)
    dual_host_ip = Column(String(), default='0.0.0.0')
    dual_host_loc = Column(Enum('none'), default='none')
    sensor_id = Column(Integer(), default=0)
    act_temp = Column(Integer(), default=0)
    tca_low = Column(Integer(), default=0)
    tca_high = Column(Integer(), default=0)
    shut_low = Column(Integer(), default=0)
    shut_high = Column(Integer(), default=0)
    restrt_cnt = Column(Integer(), default=0)
    vce_profile_id = Column(Integer(), default=None, nullable=True)
    vplt_autodiscover = Column(Enum('enabled', 'disabled'), default='disabled')
    vect_fallback_spectrum_profile = Column(Integer(), default=None)
    vect_fallback_fb_vplt_com_fail = Column(Boolean, default=False)
    vect_fallback_fb_cpe_cap_mism = Column(Boolean, default=False)
    vect_fallback_fb_conf_not_feas = Column(Boolean, default=False)

    def __repr__(self):
        return "<AlcatelCard(id='%s', name='%s', box_id='%s' and subrack_id='%s')>" %\
               (self.id, self.name, self.box_id, self.subrack_id)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_fields()
        self.set_subcomponents()

    def set_fields(self):
        self.description = "Physical card " + self.name
        self.planned_type = "rdlt-c"
        self.actual_type = "rdlt-c"
        self.operational_state = "enabled"
        self.admin_state = "unlock"
        self.err_state = "no-error"
        self.availability = "available"
        self.alarm_profile = "none"
        self.capab_profile = "32port_xDSL"
        self.manufacturer = "ALCL"
        self.mnemonic = "RDLT-C"
        self.pba_code = "3FE68863GGFL"
        self.fpba_code = "3FE68863GGFL"
        self.fpba_ics = "02"
        self.clei_code = "VBIUAALBAB"
        self.serial_no = "AA1815FSE1CG"
        self.failed_test = "00:00:00:00"
        self.lt_restart_time = "1970-01-01:00:00:00"
        self.lt_restart_cause = "poweron"
        self.lt_restart_num = 0
        self.mgnt_entity_oamipaddr = "0.0.0.0"
        self.mgnt_entity_pairnum = 0
        self.dual_host_ip = "0.0.0.0"
        self.dual_host_loc = "none"
        self.product = "xdsl"

    def set_subcomponents(self):
        ports = []
        for x in ('/1', '/2', '/3'):
            port = AlcatelPort(name=self.name + x, box_id=self.box_id)
            ports.append(port)
        self.ports = ports
