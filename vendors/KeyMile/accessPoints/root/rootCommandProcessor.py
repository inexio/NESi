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


class RootCommandProcessor(BaseCommandProcessor):
    __name__ = 'root'
    management_functions = {'main', 'cfgm', 'fm', 'status'}
    access_points = ('eoam', 'fan', 'multicast', 'services', 'tdmConnections')

    from .rootManagementFunctions import main
    from .rootManagementFunctions import cfgm
    from .rootManagementFunctions import fm
    from .rootManagementFunctions import status

    def _init_access_points(self, context=None):
        for card in self._model.cards:
            if 'unit-' + card.name in self.access_points:
                continue
            self.access_points += ('unit-' + card.name,)

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'test', str):
            ip, = self._dissect(args, 'test', str)
            #TODO test case
            return
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)