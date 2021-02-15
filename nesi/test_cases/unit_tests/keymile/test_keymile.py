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

from nesi.test_cases.unit_tests.test_core import TestCore
import pytest
from os import listdir
from os.path import isfile, join


class TestKeymile(TestCore):
    PATH = 'nesi/test_cases/integration_tests/keymile/'
    DATA = [f for f in listdir(PATH) if
            isfile(join('nesi/test_cases/integration_tests/keymile/', f)) and f != 'output.txt']

    def test_box(self):
        assert True

    def test_card(self):
        card = self.model.get_card("name", '19')
        card.set_sip('gateway_name', 'home_domain', 1, 'country_code', 'area_code', 12, 11, True,  'Asserted', False,
                     1, False, False, 1222)
        assert card.gateway_name == 'gateway_name'
        assert card.uas_request_timer is False
        card.set_ip('1.1.1.1', '2.22.2.2', '111.111.111.111')
        assert card.subnet_mask == '2.22.2.2'
        card.set_label('"l1"', '"l2"', 'desc')
        assert card.label1 == '"l1"'
        card.set_proxy('PrimaryOnly', 'proxy_address', 11, 'proxy_address_sec', 12, True,
                  'Register', 33)
        assert card.proxy_mode == 'PrimaryOnly'
        assert card.proxy_interval == 33

    def test_channel(self):
        channel = self.model.get_chan('id', 1)
        channel.set_profile_name('name')
        assert channel.chan_profile_name == 'name'

    def test_port(self):
        port = self.model.get_port('id', 1)
        port.set_profiles(True, 'n1', 1, False, 'n2', 0, True, 'dff', 11, False, 'n4', 'Priority')
        assert port.profile1_name == 'n1'
        assert port.profile1_enable is True
        port.set_test_state('Passed')
        assert port.loopbacktest_state == 'Passed'
        port.lock_admin()
        assert port.admin_state == '2'
        port.unlock_admin()
        assert port.admin_state == '3'
        port.set_melttest_state('Passed')
        assert port.melttest_state == 'Passed'
        port.set_linetest_state('Passed')
        assert port.linetest_state == 'Passed'
        port.set_mode('mode')
        assert port.mode == 'mode'
        port.set_flow_control('test')
        assert port.flow_control == 'test'

    def test_portgroupport(self):
        port = self.model.get_portgroupport('name', '19/G1/1')
        port.set_pstnport(True, True, True, 'sip', 'proxy', 'codec', 'pstn', 'enterprise')
        assert port.enable is True
        assert port.enterprise_profile == 'enterprise'
        port.set_isdnport(False, True, True, True, 'sip', 'proxy', 'codec', 'isdn')
        assert port.enable is False
        assert port.isdnba_profile == 'isdn'

    def test_srcv(self):
        srvc = self.model.get_srvc('id', 2)
        srvc.set_service('address', 11, 'CoS0', 'Add')

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
