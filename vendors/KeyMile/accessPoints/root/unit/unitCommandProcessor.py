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


class UnitCommandProcessor(BaseCommandProcessor):
    __name__ = 'unit'
    management_functions = ('main', 'cfgm', 'fm', 'status')
    access_points = () #'internalPorts', only on certain cards

    from .unitManagementFunctions import main
    from .unitManagementFunctions import cfgm
    from .unitManagementFunctions import fm
    from .unitManagementFunctions import status

    def _init_access_points(self, context=None):
        card = self._model.get_card('name', context['unit'])

        #if card.type == ?:
        #   self.access_points += ('internalPorts',)
        #

        for port in self._model.get_ports('card_id', card.id):
            identifier = 'port-' + port.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)