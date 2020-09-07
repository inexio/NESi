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

from nesi.softbox.base_resources.cpe import Cpe, CpeCollection, logging

LOG = logging.getLogger(__name__)


class AlcatelCpe(Cpe):
    """Represent physical cpe resource."""

    # alcatel specific data fields

    def admin_up(self):
        """Change cpe admin state to up."""
        self.update(admin_state='1')

    def admin_down(self):
        """Change cpe admin state to down."""
        self.update(admin_state='0')


class AlcatelCpeCollection(CpeCollection):
    """Represent a collection of cpes."""

    @property
    def _resource_type(self):
        return AlcatelCpe
