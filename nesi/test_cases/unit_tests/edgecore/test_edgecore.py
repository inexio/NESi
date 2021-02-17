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


class TestEdgecore(TestCore):
    PATH = 'nesi/test_cases/integration_tests/edgecore/'
    DATA = [f for f in listdir(PATH) if
            isfile(join('nesi/test_cases/integration_tests/edgecore/', f)) and f != 'output.txt']

    def test_box(self):
        box = self.model
        box.set('management_start_address', 'test')
        box.set('management_end_address', 'test')
        box.set('logging_host', 'test')
        box.set('logging_port', 'test')
        box.set('logging_level', 8)
        box.set('loopback_detection_action', 'shutdown')
        box.set('sntp_server_ip', '')
        box.set('sntp_client', 'Enabled')
        box.set('timezone_name', '')
        box.set('timezone_time', '')
        box.set('summer_time_name', 'test')
        box.set('summer_time_region', 'test')

        assert box.management_start_address == 'test'
        assert box.management_end_address == 'test'
        assert box.logging_host == 'test'
        assert box.logging_port == 'test'
        assert box.logging_level == 8
        assert box.loopback_detection_action == 'shutdown'
        assert box.sntp_server_ip == ''
        assert box.sntp_client == 'Enabled'
        assert box.timezone_name == ''
        assert box.timezone_time == ''
        assert box.summer_time_name == 'test'
        assert box.summer_time_region == 'test'

    def test_card(self):
        card = self.model.get_card("name", '1')
        card.set('mac_address', '11-11-11-11')
        card.set('admin_state', '1')
        card.set('operational_state', '1')

        assert card.mac_address == '11-11-11-11'
        assert card.admin_state == '1'
        assert card.operational_state == '1'

    def test_port(self):
        port = self.model.get_port("name", '1/1')
        port.set('mac_address', '11-11-11-11')
        port.set('admin_state', '1')
        port.set('operational_state', '1')

        assert port.mac_address == '11-11-11-11'
        assert port.admin_state == '1'
        assert port.operational_state == '1'

    def test_interface(self):
        interface = self.model.get_interface("name", '1/1')
        interface.set('ingress_state', 'Enabled')
        interface.set('ingress_rate', 1)
        interface.set('egress_state', 'Enabled')
        interface.set('egress_rate', 1)
        interface.set('vlan_membership_mode', 'Access')
        interface.set('native_vlan', 1010)
        interface.set('mac_address', '11-11-11-11')
        interface.set('allowed_vlan', '1,1010(u)')

        assert interface.ingress_state == 'Enabled'
        assert interface.ingress_rate == 1
        assert interface.egress_state == 'Enabled'
        assert interface.egress_rate == 1
        assert interface.vlan_membership_mode == 'Access'
        assert interface.native_vlan == 1010
        assert interface.mac_address == '11-11-11-11'
        assert interface.allowed_vlan == '1,1010(u)'

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
