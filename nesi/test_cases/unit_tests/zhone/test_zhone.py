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


class TestZhone(TestCore):

    def test_portup_portdown(self):
        port = self.model.get_port("name", '1/1/1')
        assert(self.model.get_port("name", '1/1/1').admin_state == '1')
        port.admin_down()
        assert(self.model.get_port("name", '1/1/1').admin_state == '0')
        port.admin_up()
        assert(self.model.get_port("name", '1/1/1').admin_state == '1')
        assert (self.model.get_port("name", '1/1/1').operational_state == '1')
        port.down()
        assert (self.model.get_port("name", '1/1/1').operational_state == '0')
        port.up()
        assert (self.model.get_port("name", '1/1/1').operational_state == '1')

