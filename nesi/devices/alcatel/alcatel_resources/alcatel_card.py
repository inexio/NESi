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

from nesi.devices.softbox.base_resources.card import CardCollection, Card, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class AlcatelCard(Card):
    """Represent physical shelf resource."""

    planned_type = base.Field('planned_type')
    actual_type = base.Field('actual_type')
    admin_state = base.Field('admin_state')
    operational_state = base.Field('operational_state')
    err_state = base.Field('err_state')
    availability = base.Field('availability')
    alarm_profile = base.Field('alarm_profile')
    capab_profile = base.Field('capab_profile')
    manufacturer = base.Field('manufacturer')
    mnemonic = base.Field('mnemonic')
    pba_code = base.Field('pba_code')
    fpba_code = base.Field('fpba_code')
    fpba_ics = base.Field('fpba_ics')
    clei_code = base.Field('clei_code')
    serial_no = base.Field('serial_no')
    failed_test = base.Field('failed_test')
    lt_restart_time = base.Field('lt_restart_time')
    lt_restart_cause = base.Field('lt_restart_cause')
    lt_restart_num = base.Field('lt_restart_num')
    mgnt_entity_oamipaddr = base.Field('mgnt_entity_oamipaddr')
    mgnt_entity_pairnum = base.Field('mgnt_entity_pairnum')
    dual_host_ip = base.Field('dual_host_ip')
    dual_host_loc = base.Field('dual_host_loc')
    sensor_id = base.Field('sensor_id')
    act_temp = base.Field('act_temp')
    tca_low = base.Field('tca_low')
    tca_high = base.Field('tca_high')
    shut_low = base.Field('shut_low')
    shut_high = base.Field('shut_high')
    enabled = base.Field('enabled')
    restrt_cnt = base.Field('restrt_cnt')
    position = base.Field('position')
    vce_profile_id = base.Field('vce_profile_id')
    vplt_autodiscover = base.Field('vplt_autodiscover')
    dual_tag_mode = base.Field('dual_tag_mode')
    entry_vlan_number = base.Field('entry_vlan_number')
    vect_fallback_spectrum_profile = base.Field('vect_fallback_spectrum_profile')
    vect_fallback_fb_vplt_com_fail = base.Field('vect_fallback_fb_vplt_com_fail')
    vect_fallback_fb_cpe_cap_mism = base.Field('vect_fallback_fb_cpe_cap_mism')
    vect_fallback_fb_conf_not_feas = base.Field('vect_fallback_fb_conf_not_feas')

    def set_vect_fallback_fb_vplt_com_fail(self, bool):
        """Set the cards vect_fallback_fb_vplt_com_fail value"""
        self.update(vect_fallback_fb_vplt_com_fail=bool)

    def set_vect_fallback_fb_cpe_cap_mism(self, bool):
        """Set the cards vect_fallback_fb_cpe_cap_mism value"""
        self.update(vect_fallback_fb_cpe_cap_mism=bool)

    def set_vect_fallback_fb_conf_not_feas(self, bool):
        """Set the cards vect_fallback_fb_conf_not_feas value"""
        self.update(vect_fallback_fb_conf_not_feas=bool)

    def set_vce_profile(self, profile_id):
        """Set the cards vce-profile."""
        self.update(vce_profile_id=profile_id)

    def set_vplt_autodiscover(self, value):
        """Set the cards vplt_autodiscover mode."""
        self.update(vplt_autodiscover=value)

    def set_planned_type(self, type):
        """Set the cards planned_type mode."""
        self.update(planned_type=type)

    def set_admin_state(self, state):
        """Set the cards planned_type mode."""
        self.update(admin_state=state)

    def set_dual_tag_mode(self, dual_tag_mode):
        """Change dual_tag_mode of a vlan"""
        self.update(dual_tag_mode=dual_tag_mode)

    def set_entry_vlan_number(self, entry_vlan_number):
        """Change entry_vlan_number of a vlan"""
        if self.name == 'nt-a' or self.name == 'nt-b':
            self.update(entry_vlan_number=entry_vlan_number)

    def set_vect_fallback_spectrum_profile(self, profile_id):
        """Change the vect_fallback_spectrum_profile of a card"""
        self.update(vect_fallback_spectrum_profile=profile_id)



class AlcatelCardCollection(CardCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return AlcatelCard
