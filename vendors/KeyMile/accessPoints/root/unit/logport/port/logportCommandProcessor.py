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


class LogportCommandProcessor(PortCommandProcessor):
    __name__ = 'logport'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status', 'ifMIB')
    access_points = ()

    from .logportManagementFunctions import main
    from .logportManagementFunctions import cfgm
    from .logportManagementFunctions import fm
    from .logportManagementFunctions import pm
    from .logportManagementFunctions import status
    from .logportManagementFunctions import ifMIB

    def get_property(self, command, *args, context=None):
        port = self.get_port_component()
        scopes = ('login', 'base', 'get')
        try:
            super().get_property(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'AttainableRate') and context['component_path'].split('/')[-1] == 'status':
                text = self._render('attainable_rate', *scopes, context=context)
                self._write(text)
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def get_port_component(self):
        return self._model.get_logport('name', self._parent._parent.component_id + '/L/' + self.component_id)

    def _init_access_points(self, context=None):
        logport_name = self._parent._parent.component_id + '/L/' + self.component_id
        logport = self._model.get_logport('name', logport_name)
        try:
            _ = self._model.get_interface('logport_id', logport.id)
        except exceptions.SoftboxenError:
            pass
        else:
            for interface in self._model.get_interfaces('logport_id', logport.id):
                identifier = 'interface-' + interface.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        try:
            super().set(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate(args, *()):
                exc = exceptions.CommandSyntaxError(command=command)
                exc.template = 'syntax_error'
                exc.template_scopes = ('login', 'base', 'syntax_errors')
                raise exc
            elif self._validate(args, 'test', str):
                ip, = self._dissect(args, 'test', str)
                # TODO test case
                return
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
