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

from nesi.devices.softbox.api.schemas.card_schemas import *


class AlcatelCardSchema(CardSchema):
    class Meta:
        model = Card
        fields = CardSchema.Meta.fields + ('planned_type', 'actual_type', 'admin_state', 'operational_state',
                                           'err_state', 'availability', 'alarm_profile', 'capab_profile',
                                           'manufacturer', 'mnemonic', 'pba_code', 'fpba_code', 'fpba_ics',
                                           'clei_code', 'serial_no', 'failed_test', 'lt_restart_time',
                                           'lt_restart_cause', 'lt_restart_num', 'mgnt_entity_oamipaddr',
                                           'mgnt_entity_pairnum', 'dual_host_ip', 'dual_host_loc', 'sensor_id',
                                           'act_temp', 'tca_low', 'tca_high', 'shut_low', 'shut_high', 'enabled',
                                           'restrt_cnt', 'position', 'dual_tag_mode', 'entry_vlan_number',
                                           'vplt_autodiscover', 'vce_profile_id', 'vect_fallback_spectrum_profile',
                                           'vect_fallback_fb_vplt_com_fail', 'vect_fallback_fb_cpe_cap_mism',
                                           'vect_fallback_fb_conf_not_feas')
