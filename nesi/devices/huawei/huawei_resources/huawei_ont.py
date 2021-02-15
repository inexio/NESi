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

from nesi.devices.softbox.base_resources.ont import Ont, OntCollection
from nesi.devices.softbox.base_resources import base


class HuaweiOnt(Ont):
    """Represent physical shelf resource."""

    serial_number = base.Field('serial_number')
    control_flag = base.Field('control_flag')
    config_state = base.Field('config_state')
    match_state = base.Field('match_state')
    protect_side = base.Field('protect_side')
    dba_type = base.Field('dba_type')
    ont_distance = base.Field('ont_distance')
    ont_last_distance = base.Field('ont_last_distance')
    ont_battery_state = base.Field('ont_battery_state')
    memory_occupation = base.Field('memory_occupation')
    cpu_occupation = base.Field('cpu_occupation')
    temperature = base.Field('temperature')
    authentic_type = base.Field('authentic_type')
    management_mode = base.Field('management_mode')
    software_work_mode = base.Field('software_work_mode')
    isolation_state = base.Field('isolation_state')
    ont_ip_zero_address_mask = base.Field('ont_ip_zero_address_mask')
    last_down_cause = base.Field('last_down_cause')
    last_up_time = base.Field('last_up_time')
    last_down_time = base.Field('last_down_time')
    last_dying_gasp = base.Field('last_dying_gasp')
    ont_online_duration = base.Field('ont_online_duration')
    type_c_support = base.Field('type_c_support')
    interoperability_mode = base.Field('interoperability_mode')
    power_reduction_status = base.Field('power_reduction_status')
    fec_upstream_state = base.Field('fec_upstream_state')
    index = base.Field('index')
    port_number_pots = base.Field('port_number_pots')
    max_adaptive_num_pots = base.Field('max_adaptive_num_pots')
    port_number_eth = base.Field('port_number_eth')
    max_adaptive_num_eth = base.Field('max_adaptive_num_eth')
    port_number_vdsl = base.Field('port_number_vdsl')
    max_adaptive_num_vdsl = base.Field('max_adaptive_num_vdsl')
    lineprofile_id = base.Field('lineprofile_id')
    srvprofile_id = base.Field('srvprofile_id')
    version = base.Field('version')
    vendor_id = base.Field('vendor_id')
    software_version = base.Field('software_version')

    def set_online_duration(self, duration):
        """Set the ont online duration"""
        self.update(ont_online_duration=duration)


class HuaweiOntCollection(OntCollection):
    """Represent a collection of ONTs."""

    @property
    def _resource_type(self):
        return HuaweiOnt
