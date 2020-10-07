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
from vendors.KeyMile.accessPoints.root.unit.port.portCommandProcessor import PortCommandProcessor


class LogPortCommandProcessor(PortCommandProcessor):
    __name__ = 'logport'
    management_functions = ('main', 'cfgm', 'status')
    access_points = ()

    from .logportManagementFunctions import main
    from .logportManagementFunctions import cfgm
    from .logportManagementFunctions import status

    def do_get(self, command, *args, context=None):
        scopes = ('login', 'base', 'get')
        try:
            super().do_get(command, *args, context=None)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'AttainableRate') and context['path'].split('/')[-1] == 'status':
                text = self._render('attainable_rate', *scopes, context=context)
                self._write(text)
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        port = self._model.get_port('name', context['unit'] + '/' + context['portgroup'] + '/' + context['port'])

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        try:
            super().set(command, *args, context=None)
        except exceptions.CommandExecutionError:
            if self._validate(args, *()):
                exc = exceptions.CommandSyntaxError(command=command)
                exc.template = 'syntax_error'
                exc.template_scopes = ('login', 'base', 'syntax_errors')
                raise exc
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
