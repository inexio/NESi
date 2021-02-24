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


class TestPbn(TestCore):
    PATH = 'nesi/test_cases/integration_tests/pbn/'
    DATA = [f for f in listdir('nesi/test_cases/integration_tests/pbn/') if
            isfile(join('nesi/test_cases/integration_tests/pbn/', f)) and f != 'output.txt']

    def test_box(self):
        assert True

    def test_user(self):
        user = self.model.get_user('id', 1)
        user.set_online()
        assert user.status == 'online'
        user.set_offline()
        assert user.status == 'offline'

    def test_port(self):
        port = self.model.get_port('id', 1)
        port.set('description', '')
        assert port.description == ''
        port.set('spanning_tree_guard_root', True)
        assert port.spanning_tree_guard_root is True
        port.set('switchport_trunk_vlan_allowed', None)
        assert port.switchport_trunk_vlan_allowed is None
        port.set('switchport_mode_trunk', True)
        assert port.switchport_mode_trunk is True
        port.set('switchport_pvid', None)
        assert port.switchport_pvid is None
        port.set('no_lldp_transmit', True)
        assert port.no_lldp_transmit is True
        port.set('pbn_speed', 1)
        assert port.pbn_speed == 1
        port.set('switchport_block_multicast', True)
        assert port.switchport_block_multicast is True
        port.set('switchport_rate_limit_egress', None)
        assert port.switchport_rate_limit_egress is None
        port.set('switchport_rate_limit_ingress', None)
        assert port.switchport_rate_limit_ingress is None
        port.set('exclamation_mark', True)
        assert port.exclamation_mark is True

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
