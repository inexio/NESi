
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

