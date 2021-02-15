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

from nesi.devices.softbox.api.schemas.ont_schemas import *


class HuaweiOntSchema(OntSchema):
    class Meta:
        model = Ont
        fields = OntSchema.Meta.fields + ('serial_number', 'control_flag', 'config_state', 'match_state',
                                          'protect_side', 'dba_type', 'ont_distance', 'ont_last_distance',
                                          'ont_battery_state', 'memory_occupation', 'cpu_occupation', 'temperature',
                                          'authentic_type', 'management_mode', 'software_work_mode', 'isolation_state',
                                          'ont_ip_zero_address_mask', 'last_down_cause', 'last_up_time',
                                          'last_down_time', 'last_dying_gasp', 'ont_online_duration', 'type_c_support',
                                          'interoperability_mode', 'power_reduction_status', 'fec_upstream_state',
                                          'port_number_pots', 'max_adaptive_num_pots', 'port_number_eth',
                                          'max_adaptive_num_eth', 'port_number_vdsl', 'max_adaptive_num_vdsl',
                                          'lineprofile_id', 'srvprofile_id', 'index', 'version',
                                          'software_version', 'vendor_id')
