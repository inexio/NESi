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


class ChanCommandProcessor(BaseCommandProcessor):
    __name__ = 'chan'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .chanManagementFunctions import main
    from .chanManagementFunctions import cfgm
    from .chanManagementFunctions import fm
    from .chanManagementFunctions import pm
    from .chanManagementFunctions import status

    def _init_access_points(self, context=None):
        chan = self._model.get_chan('name', context['unit'] + '/' + context['port'] + '/' + context['chan'])
        card = self._model.get_card('name', context['unit'])

        for interface in self._model.get_interfaces('chan_id', chan.id):
            if card.product != 'adsl':
                ap_name = 'interface-'
            else:
                ap_name = 'vcc-'
            identifier = ap_name + interface.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)