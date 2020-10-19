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

from nesi.softbox.base_resources.port import PortCollection, Port, logging, base

LOG = logging.getLogger(__name__)


class KeyMilePort(Port):
    """Represent physical port resource."""
    label1 = base.Field('label1')
    label2 = base.Field('label2')
    loopbacktest_state = base.Field('loopbacktest_state')
    melttest_state = base.Field('melttest_state')
    linetest_state = base.Field('linetest_state')

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)

    def set_test_state(self, state):
        self.update(loopbacktest_state=state)

    def lock_admin(self):
        """Set the admin port state to up"""
        self.update(admin_state='2')

    def unlock_admin(self):
        """Set the admin port state to down"""
        self.update(admin_state='3')

    def set_melttest_state(self, state):
        self.update(melttest_state=state)

    def set_linetest_state(self, state):
        self.update(linetest_state=state)


class KeyMilePortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return KeyMilePort
