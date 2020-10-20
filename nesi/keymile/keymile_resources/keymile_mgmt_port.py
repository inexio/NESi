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

from nesi.softbox.base_resources.mgmt_port import MgmtPortCollection, MgmtPort, logging, base

LOG = logging.getLogger(__name__)


class KeyMileMgmtPort(MgmtPort):
    """Represent physical port resource."""
    label1 = base.Field('label1')
    label2 = base.Field('label2')

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)


class KeyMileMgmtPortCollection(MgmtPortCollection):
    """Represent a collection of ports."""

    @property
    def _resource_type(self):
        return KeyMileMgmtPort
