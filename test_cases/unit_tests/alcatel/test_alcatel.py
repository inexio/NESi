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

from test_cases.unit_tests.test_core import TestCore
from os import listdir
from os.path import isfile, join
import pytest
from nesi import exceptions


class TestAlcatel(TestCore):
    PATH = 'test_cases/integration_tests/alcatel/'
    DATA = [f for f in listdir('test_cases/integration_tests/alcatel/') if
            isfile(join('test_cases/integration_tests/alcatel/', f)) and f != 'output.txt']

    def test_ontportup_portdown(self):
        port = self.model.get_ont_port("name", '1/1/4/2/1/1/1')
        assert (self.model.get_ont_port("name", '1/1/4/2/1/1/1').admin_state == '0')
        port.admin_up()
        assert (self.model.get_ont_port("name", '1/1/4/2/1/1/1').admin_state == '1')
        port.admin_down()
        assert (self.model.get_ont_port("name", '1/1/4/2/1/1/1').admin_state == '0')

    def test_card_types(self):
        card = self.model.get_card("name", '1/1/1')
        assert card.planned_type == 'rdlt-c'
        card.set_planned_type('empty')
        assert card.planned_type == 'empty'
        card.set_planned_type('nant-a')
        assert card.planned_type == 'nant-a'
        card.set_planned_type('fant-f')
        assert card.planned_type == 'fant-f'
        try:
            card.set_planned_type('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_card_vect(self):
        card = self.model.get_card("name", '1/1/1')
        assert card.vect_fallback_fb_vplt_com_fail is False
        card.set_vect_fallback_fb_vplt_com_fail(True)
        assert card.vect_fallback_fb_vplt_com_fail is True
        try:
            card.set_vect_fallback_fb_vplt_com_fail('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.vect_fallback_fb_cpe_cap_mism is False
        card.set_vect_fallback_fb_cpe_cap_mism(True)
        assert card.vect_fallback_fb_cpe_cap_mism is True
        try:
            card.set_vect_fallback_fb_cpe_cap_mism('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.vect_fallback_fb_conf_not_feas is False
        card.set_vect_fallback_fb_conf_not_feas(True)
        assert card.vect_fallback_fb_conf_not_feas is True
        try:
            card.set_vect_fallback_fb_conf_not_feas('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.vect_fallback_spectrum_profile is None
        card.set_vect_fallback_spectrum_profile(1)
        assert card.vect_fallback_spectrum_profile == 1
        try:
            card.set_vect_fallback_spectrum_profile('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_card_rest(self):
        card = self.model.get_card("name", '1/1/1')

        assert card.vce_profile_id is None
        card.set_vce_profile(1)
        assert card.vce_profile_id == 1
        try:
            card.set_vce_profile('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.vplt_autodiscover == 'disabled'
        card.set_vplt_autodiscover('enabled')
        assert card.vplt_autodiscover == 'enabled'
        try:
            card.set_vplt_autodiscover('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.admin_state == '1'
        card.set_admin_state('0')
        assert card.admin_state == '0'
        try:
            card.set_admin_state('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.dual_tag_mode is False
        card.set_dual_tag_mode(True)
        assert card.dual_tag_mode is True
        try:
            card.set_dual_tag_mode('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert card.entry_vlan_number is None
        card.set_entry_vlan_number(1)
        assert card.entry_vlan_number is None

    def test_mngt_card(self):
        card = self.model.get_card("name", 'nt-a')

        assert card.entry_vlan_number is None
        card.set_entry_vlan_number(1)
        assert card.entry_vlan_number == 1

    def test_port_states(self):
        port = self.model.get_port("name", '1/1/1/3')
        assert (port.admin_state == '0')
        port.admin_up()
        assert (port.admin_state == '1')
        port.admin_down()
        assert (port.admin_state == '0')
        port.admin_up()
        assert (port.admin_state == '1')
        port.down()
        assert (port.operational_state == '0')
        port.up()
        assert (port.operational_state == '1')

    def test_port_rest(self):
        port = self.model.get_port("name", '1/1/1/1')

        assert port.description == 'Physical port 1/1/1/1'
        port.set_description('this is a port')
        assert port.description == 'this is a port'
        try:
            port.set_description(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.egress_port is False
        port.set_egress_port(True)
        assert port.egress_port is True
        try:
            port.set_egress_port('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.service_profile_id is None
        assert port.spectrum_profile_id is None
        assert port.vect_profile_id is None
        assert port.dpbo_profile_id is None
        port.update_profile(1, 'service')
        port.update_profile(1, 'spectrum')
        port.update_profile(1, 'vect')
        port.update_profile(1, 'dpbo')
        assert port.service_profile_id == 1
        assert port.spectrum_profile_id == 1
        assert port.vect_profile_id == 1
        assert port.dpbo_profile_id == 1
        try:
            port.update_profile('lala', 'dpbo')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_cpe_states(self):
        port = self.model.get_cpe("name", '1/1/1/1/1')
        assert (port.admin_state == '1')
        port.admin_down()
        assert (port.admin_state == '0')
        port.admin_up()
        assert (port.admin_state == '1')

    def test_ont_states(self):
        port = self.model.get_ont("name", '1/1/4/1/1')
        port.power_down()
        assert (port.admin_state == '0')
        assert (port.operational_state == '0')
        port.admin_up()
        assert (port.admin_state == '1')
        assert (port.operational_state == '0')
        port.admin_down()
        assert (port.admin_state == '0')
        port.power_up()
        assert (port.admin_state == '1')
        assert (port.operational_state == '1')

    def test_ont_rest(self):
        port = self.model.get_ont("name", '1/1/4/1/1')
        assert (port.type == "10gbaselr")
        port.set_type('1000baselx10')
        assert port.type == '1000baselx10'
        try:
            port.set_type('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.auto_neg_supported is False)
        assert (port.auto_neg_status == 'disabled')
        port.autonegotiate()
        assert (port.auto_neg_supported is True)
        assert (port.auto_neg_status == 'complete')

        assert (port.cap1000base_xfd == 'yes')
        port.set_cap1000base_xfd('no')
        assert (port.cap1000base_xfd == 'no')
        try:
            port.set_cap1000base_xfd('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_ontport_states(self):
        port = self.model.get_ont_port("name", '1/1/4/1/1/1/1')
        assert (port.admin_state == '1')
        port.admin_down()
        assert (port.admin_state == '0')
        port.admin_up()
        assert (port.admin_state == '1')
        assert (port.operational_state == '0')
        port.port_up()
        assert (port.operational_state == '1')
        port.port_down()
        assert (port.operational_state == '0')

    def test_ontport_rest(self):
        port = self.model.get_ont_port("name", '1/1/4/1/1/1/1')
        assert (port.description == 'OntPort 1/1/4/1/1/1/1')
        port.set_description('this is a ontport')
        assert (port.description == 'this is a ontport')
        try:
            port.set_description(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.speed == '1000')
        port.set_speed('1')
        assert (port.speed == '1')
        try:
            port.set_speed(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_serviceport_fields(self):
        port = self.model.get_service_port("name", '1/1/1/1')
        assert port.max_unicast_mac is None
        port.set_max_unicast_mac(1)
        assert port.max_unicast_mac == 1
        try:
            port.set_max_unicast_mac('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.qos_profile_id is None
        port.set_qos_profile(1)
        assert port.qos_profile_id == 1
        try:
            port.set_qos_profile('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.pvid is None
        port.set_pvid(1)
        assert port.pvid == 1
        try:
            port.set_pvid('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_serviceport_fields(self):
        port = self.model.get_service_vlan("name", '2620')
        assert port.l2fwder_vlan is None
        port.set_l2fwder_vlan(1)
        assert port.l2fwder_vlan == 1
        try:
            port.set_l2fwder_vlan('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.scope == 'local')
        port.set_scope(None)
        assert (port.scope is None)
        port.set_scope('local')
        try:
            port.set_scope(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.tag == 'single-tagged')
        port.set_tag('untagged')
        assert (port.tag == 'untagged')
        try:
            port.set_tag(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_vlan_name(self):
        port = self.model.get_vlan("name", 'PPPoE')
        port.change_name('PEPE')
        assert (port.name == 'PEPE')
        try:
            self.model.get_vlan("name", 'PPPoE')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_vlan_fields(self):
        port = self.model.get_vlan("id", 1)
        assert (port.pppoe_relay_tag == 'configurable')
        port.set_pppoe_relay_tag('not configurable')
        assert (port.pppoe_relay_tag == 'not configurable')
        try:
            port.set_pppoe_relay_tag(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.protocol_filter == 'pass-pppoe')
        port.set_protocol_filter('not configurable')
        assert (port.protocol_filter == 'not configurable')
        try:
            port.set_protocol_filter(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.new_broadcast == 'disable')
        port.set_new_broadcast('enable')
        assert (port.new_broadcast == 'enable')
        try:
            port.set_new_broadcast('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.new_secure_fwd == 'disable')
        port.set_new_secure_fwd('enable')
        assert (port.new_secure_fwd == 'enable')
        try:
            port.set_new_secure_fwd('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.aging_time is None
        port.set_aging_time(1)
        assert port.aging_time == 1
        try:
            port.set_aging_time('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.circuit_id_dhcp is None
        port.set_circuit_id_dhcp('1')
        assert port.circuit_id_dhcp == '1'
        try:
            port.set_circuit_id_dhcp(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.remote_id_dhcp is None
        port.set_remote_id_dhcp('1')
        assert port.remote_id_dhcp == '1'
        try:
            port.set_remote_id_dhcp(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.dhcp_opt82_ext == 'disable')
        port.set_dhcp_opt82_ext('enable')
        assert (port.dhcp_opt82_ext == 'enable')
        try:
            port.set_dhcp_opt82_ext('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.dhcp_opt82 == 'disable')
        port.set_dhcp_opt82('enable')
        assert (port.dhcp_opt82 == 'enable')
        try:
            port.set_dhcp_opt82('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.pppoe_linerate == 'addactuallinerate')
        port.set_pppoe_linerate('enable')
        assert (port.pppoe_linerate == 'enable')
        try:
            port.set_pppoe_linerate(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.circuit_id_pppoe == 'physical-id')
        port.set_circuit_id_pppoe('enable')
        assert (port.circuit_id_pppoe == 'enable')
        try:
            port.set_circuit_id_pppoe(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.remote_id_pppoe == 'customer-id')
        port.set_remote_id_pppoe('enable')
        assert (port.remote_id_pppoe == 'enable')
        try:
            port.set_remote_id_pppoe(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.mode == 'residential-bridge')
        port.set_mode('reserved')
        assert (port.mode == 'reserved')
        try:
            port.set_mode('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.tag == 'untagged')
        port.set_tag('tagged')
        assert (port.tag == 'tagged')
        try:
            port.set_tag('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.egress_port == '')
        port.set_egress_port('tagged')
        assert (port.egress_port == 'tagged')
        try:
            port.set_egress_port(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert (port.in_qos_prof_name == 'name:Default_TC0')
        port.set_in_qos_prof_name('tagged')
        assert (port.in_qos_prof_name == 'tagged')
        try:
            port.set_in_qos_prof_name(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_box_properties(self):
        assert len(self.model.subracks) == 1
        assert len(self.model.cards) == 6
        assert len(self.model.get_cards()) == 6
        assert len(self.model.ports) == 14
        assert len(self.model.onts) == 5
        assert len(self.model.ont_ports) == 6
        assert len(self.model.cpes) == 12
        assert len(self.model.cpe_ports) == 12
        assert len(self.model.vlans) == 2
        assert len(self.model.service_vlans) == 41
        assert len(self.model.service_ports) == 22
        assert len(self.model.credentials) == 1
        assert len(self.model.routes) == 0
        assert len(self.model.port_profiles) == 14
        assert len(self.model.qos_interfaces) == 0

    def test_box_add_resources(self):
        count = len(self.model.vlans)
        self.model.add_vlan(name='lala', number=10101)
        self.model.add_vlan(name='test_vlan2', number=9999, shutdown=False, tag='tagged')
        assert count + 2 == len(self.model.vlans)
        try:
            broken_vlan = self.model.add_vlan(tag='untagged')
            assert False
        except exceptions.SoftboxenError:
            assert True
        assert count + 2 == len(self.model.vlans)

        count = len(self.model.service_ports)
        self.model.add_service_port(name='test_sport', connected_id=2, connected_type='port')
        assert count+1 == len(self.model.service_ports)
        try:
            broken_sport = self.model.add_service_port(name='test_sport2')
            assert False
        except exceptions.SoftboxenError:
            assert True
        assert count+1 == len(self.model.service_ports)

        count = len(self.model.qos_interfaces)
        self.model.add_qos_interface(name='test_qos')
        assert count+1 == len(self.model.qos_interfaces)

        count = len(self.model.service_vlans)
        self.model.add_service_vlan(name='test_svlan', vlan_id=1, card_id=1)
        self.model.add_service_vlan(name='test_svlan1', vlan_id=1, service_port_id=1)
        assert count+2 == len(self.model.service_vlans)
        try:
            broken_sport = self.model.add_service_vlan(name='test_svlan2')
            assert False
        except exceptions.SoftboxenError:
            assert True
        assert count+2 == len(self.model.service_vlans)

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
