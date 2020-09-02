
from test_cases.unit_tests.test_core import TestCore


class TestHuawei(TestCore):

    def test_portup_portdown(self):
        port = self.model.get_port("name", '0/0/0')
        assert(self.model.get_port("name", '0/0/0').admin_state == 'deactivated')
        port.admin_up()
        assert(self.model.get_port("name", '0/0/0').admin_state == 'activated')
        port.admin_down()
        assert(self.model.get_port("name", '0/0/0').admin_state == 'deactivated')

    def test_ontportup_portdown(self):
        port = self.model.get_ont_port("name", '0/2/0/0/1')
        assert(self.model.get_ont_port("name", '0/2/0/0/1').operational_state == 'down')
        port.operational_state_up()
        assert(self.model.get_ont_port("name", '0/2/0/0/1').operational_state == 'up')
        port.operational_state_down()
        assert(self.model.get_ont_port("name", '0/2/0/0/1').operational_state == 'down')

