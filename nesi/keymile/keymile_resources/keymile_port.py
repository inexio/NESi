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
    mode = base.Field('mode')
    flow_control = base.Field('flow_control')
    profile1_enable = base.Field('profile1_enable')
    profile1_name = base.Field('profile1_name')
    profile1_elength = base.Field('profile1_elength')
    profile2_enable = base.Field('profile2_enable')
    profile2_name = base.Field('profile2_name')
    profile2_elength = base.Field('profile2_elength')
    profile3_enable = base.Field('profile3_enable')
    profile3_name = base.Field('profile3_name')
    profile3_elength = base.Field('profile3_elength')
    profile4_enable = base.Field('profile4_enable')
    profile4_name = base.Field('profile4_name')
    profile_mode = base.Field('profile_mode')
    upstream = base.Field('upstream')
    downstream = base.Field('downstream')

    def set_profile(self, name):
        self.update(profile1_name=name)


    def set_profiles(self, e1, n1, el1, e2, n2, el2, e3, n3, el3, e4, n4, mode):
        self.update(profile1_enable=e1)
        self.update(profile1_name=n1)
        self.update(profile1_elength=el1)
        self.update(profile2_enable=e2)
        self.update(profile2_name=n2)
        self.update(profile2_elength=el2)
        self.update(profile3_enable=e3)
        self.update(profile3_name=n3)
        self.update(profile3_elength=el3)
        self.update(profile4_enable=e4)
        self.update(profile4_name=n4)
        self.update(profile_mode=mode)

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

    def set_mode(self, mode):
        self.update(mode=mode)

    def set_flow_control(self, ctrl):
        self.update(flow_control=ctrl)


class KeyMilePortCollection(PortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return KeyMilePort
