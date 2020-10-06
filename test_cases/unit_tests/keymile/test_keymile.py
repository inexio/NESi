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
import pytest
from os import listdir
from os.path import isfile, join


class TestKeymile(TestCore):
    PATH = 'test_cases/integration_tests/keymile/'
    DATA = [f for f in listdir('test_cases/integration_tests/keymile/') if
            isfile(join('test_cases/integration_tests/keymile/', f)) and f != 'output.txt']

    def test_box(self):
        assert True

    def test_card(self):
        assert True

    def test_channel(self):
        assert True

    def test_interface(self):
        assert True

    def test_port(self):
        assert True

    def test_subrack(self):
        assert True

    @pytest.mark.parametrize("path", DATA)
    def test_integration(self, path):
        self.run(self.PATH + path, self.PATH + 'output.txt')
