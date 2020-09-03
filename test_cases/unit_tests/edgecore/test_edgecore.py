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


class TestEdgecore(TestCore):

    def test_portup_portdown(self):
        port = self.model.get_port("name", '1/1/1/1')
        assert(self.model.get_port("name", '1/1/1/1').admin_state == 'down')
        port.admin_up()
        assert(self.model.get_port("name", '1/1/1/1').admin_state == 'up')
        port.admin_down()
        assert(self.model.get_port("name", '1/1/1/1').admin_state == 'down')

    def test_ontportup_portdown(self):
        port = self.model.get_ont_port("name", '1/1/4/1/1/1/1')
        assert(self.model.get_ont_port("name", '1/1/4/1/1/1/1').admin_state == 'down')
        port.admin_up()
        assert(self.model.get_ont_port("name", '1/1/4/1/1/1/1').admin_state == 'up')
        port.admin_down()
        assert(self.model.get_ont_port("name", '1/1/4/1/1/1/1').admin_state == 'down')

