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

from nesi import exceptions
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class FanCommandProcessor(BaseCommandProcessor):
    __name__ = 'fan'
    management_functions = ('main', 'cfgm', 'fm')
    access_points = ()

    from .fanManagementFunctions import main
    from .fanManagementFunctions import cfgm
    from .fanManagementFunctions import fm

    def _init_access_points(self, context=None):
        for i in range(1, 12):
            identifier = 'alarm-' + str(i)
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def _init_context(self, context=None):
        context['ls_Name'] = 'FANU4'
        context['ls_MainMode'] = ''
        context['ls_EquipmentState'] = 'Ok'
