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
from nesi import exceptions
from os import listdir
from os.path import isfile, join
import pytest


class TestHuawei(TestCore):
    PATH = 'test_cases/integration_tests/huawei/'
    DATA = [f for f in listdir('test_cases/integration_tests/huawei/') if
            isfile(join('test_cases/integration_tests/huawei/', f)) and f != 'output.txt']

    def test_portup_portdown(self):
        port = self.model.get_port("name", '0/0/0')
        port.admin_down()
        assert(self.model.get_port("name", '0/0/0').admin_state == '0')
        port.admin_up()
        assert(self.model.get_port("name", '0/0/0').admin_state == '2')
        port.up()
        assert port.operational_state == '1'
        port.down()
        assert port.operational_state == '0'

    def test_port_rest(self):
        port = self.model.get_port("name", '0/0/0')
        assert port.downstream_max == 100000
        port.port_downstream_set(1)
        assert port.downstream_max == 1
        try:
            port.port_downstream_set('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.upstream_max == 100000
        port.port_upstream_set(1)
        assert port.upstream_max == 1
        try:
            port.port_upstream_set('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.vlan_id is None
        port.set_vlan_id(1)
        assert port.vlan_id == 1
        try:
            port.set_vlan_id('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_ont_fields(self):
        port = self.model.get_ont("name", '0/2/0/0')
        assert port.ont_online_duration is None
        port.set_online_duration('1')
        assert (port.ont_online_duration == '1')
        try:
            port.set_online_duration(5)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_ont_ports(self):
        port = self.model.get_ont_port("name", '0/2/0/0/1')
        port.up()
        assert (port.admin_state == '1')
        port.down()
        assert (port.admin_state == '0')

    def test_port_profiles(self):
        port = self.model.get_port_profile("name", "PPPoE")
        assert port.type == 'service'
        port.set('type', 'spectrum')
        assert port.type == 'spectrum'
        try:
            port.set('FAIL', 'failure')
            assert False
        except exceptions.SoftboxenError:
            assert True
        port.set('type', 'service')

    def test_service_port(self):
        port = self.model.get_service_port("name", "0/0/0")
        assert port.vpi == '-'
        port.set_vpi('vpi')
        assert port.vpi == 'vpi'
        try:
            port.set_vpi(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.vci == '-'
        port.set_vci('vci')
        assert port.vci == 'vci'
        try:
            port.set_vci(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.inbound_table_name == 'ip-traffic-table_520'
        port.set_inbound_table_name('vci')
        assert port.inbound_table_name == 'vci'
        try:
            port.set_inbound_table_name(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.outbound_table_name == 'ip-traffic-table_560'
        port.set_outbound_table_name('vci')
        assert port.outbound_table_name == 'vci'
        try:
            port.set_outbound_table_name(1)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.connected_id is not None
        assert port.connected_type is not None
        id = port.connected_id
        type =port.connected_type
        port.set_connected_id(20)
        assert port.connected_id == 20
        port.set_connected_type('ont')
        assert port.connected_type == 'ont'
        try:
            port.set_connected_type(1)
            assert False
        except exceptions.SoftboxenError:
            assert True
        try:
            port.set_connected_id('failure')
            assert False
        except exceptions.SoftboxenError:
            assert True
        port.set_connected_id(id)
        port.set_connected_type(type)
        port.set_admin_state('0')
        assert port.admin_state == '0'
        port.set_admin_state('1')
        assert port.admin_state == '1'
        try:
            port.set_admin_state(0)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_service_vlan(self):
        port = self.model.get_service_vlan("name", "2620")

        assert port.mode == 'ptm'
        port.set_mode('atm')
        assert port.mode == 'atm'
        try:
            port.set_mode('fail')
            assert False
        except exceptions.SoftboxenError:
            assert True
        try:
            port.set_mode(0)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert port.tag == 'single-tagged'
        port.set_tag('untagged')
        assert port.tag == 'untagged'
        try:
            port.set_tag('fail')
            assert False
        except exceptions.SoftboxenError:
            assert True
        try:
            port.set_tag(0)
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_user(self):
        user = self.model.get_user("name", 'root')
        assert user.lock_status == 'Unlocked'
        user.lock()
        assert user.lock_status == 'Locked'
        user.unlock()
        assert user.lock_status == 'Unlocked'

        assert user.reenter_num_temp == 3
        user.set_reenter_num_temp(1)
        assert user.reenter_num_temp == 1
        try:
            user.set_reenter_num_temp('fail')
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert user.status == 'Offline'
        user.set_online()
        assert user.status == 'Online'
        user.set_offline()
        assert user.status == 'Offline'

    def test_vlan(self):
        vlan = self.model.get_vlan('number', 2620)

        assert vlan.type == 'smart'
        vlan.set_type_smart()
        assert vlan.type == 'smart'

        assert vlan.tag == 'untagged'
        vlan.set_tag('tagged')
        assert vlan.tag == 'tagged'
        try:
            vlan.set_tag('fail')
            assert False
        except exceptions.SoftboxenError:
            assert True
        try:
            vlan.set_tag(0)
            assert False
        except exceptions.SoftboxenError:
            assert True

        assert vlan.bind_service_profile_id == 1
        vlan.set_service_profile_id(22)
        assert vlan.bind_service_profile_id == 22
        try:
            vlan.set_service_profile_id('fail')
            assert False
        except exceptions.SoftboxenError:
            assert True
        vlan.set_service_profile_id(1)

    def test_vlaninterface(self):
        port = self.model.get_vlan_interface("name", "vlanif2620")
        assert port.admin_state == '1'
        port.set('admin_state', '0')
        assert port.admin_state == '0'
        try:
            port.set('FAIL', 'failure')
            assert False
        except exceptions.SoftboxenError:
            assert True

    def test_box_properties(self):
        assert len(self.model.subracks) == 1
        assert len(self.model.cards) == 5
        assert len(self.model.ports) == 13
        assert len(self.model.onts) == 8
        assert len(self.model.ont_ports) == 9
        assert len(self.model.cpes) == 11
        assert len(self.model.cpe_ports) == 11
        assert len(self.model.vlans) == 2
        assert len(self.model.service_vlans) == 1
        assert len(self.model.service_ports) == 1
        assert len(self.model.credentials) == 1
        assert len(self.model.routes) == 0
        assert len(self.model.port_profiles) == 1
        assert len(self.model.emus) == 2
        assert len(self.model.users) == 1
        assert len(self.model.vlan_interfaces) == 1

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
