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


class PortCommandProcessor(BaseCommandProcessor):
    __name__ = 'port'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .portManagementFunctions import main
    from .portManagementFunctions import cfgm
    from .portManagementFunctions import fm
    from .portManagementFunctions import pm
    from .portManagementFunctions import status

    def get_property(self, command, *args, context=None):
        port_name = self._parent.component_id + '/' + self.component_id
        port = self._model.get_port('name', port_name)
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'AttainableRate') and (context['path'].split('/')[-1] == 'status'
                                                         or context['component_path'].split('/')[-1] == 'status'):
            text = self._render('attainable_rate', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'AdministrativeStatus') and (context['path'].split('/')[-1] == 'main'
                                                               or context['component_path'].split('/')[-1] == 'main'):
            self.map_states(port, 'port')
            context['spacer'] = self.create_spacers((67,), (port.admin_state,))[0] * ' '
            text = self._render('administrative_status', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'OperationalStatus') and (context['path'].split('/')[-1] == 'main'
                                                            or context['component_path'].split('/')[-1] == 'main'):
            self.map_states(port, 'port')
            port_operational_state = port.operational_state
            context['port_operational_state'] = port_operational_state
            context['spacer'] = self.create_spacers((67,), (port_operational_state,))[0] * ' '
            text = self._render('operational_status', *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        port = self._model.get_port('name', self._parent.component_id + '/' + self.component_id)

        for chan in self._model.get_chans('port_id', port.id):
            identifier = 'chan-' + chan.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def get_port_component(self):
        return self._model.get_port('name', self._parent.component_id + '/' + self.component_id)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        print(context['path'])
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'AdministrativeStatus', str) and context['path'].split('/')[-1] == 'main':
            state, = self._dissect(args, 'AdministrativeStatus', str)
            try:
                port = self.get_port_component()
                if state == 'up':
                    port.admin_up()
                elif state == 'down':
                    port.admin_down()
                else:
                    raise exceptions.SoftboxenError()
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        else:
            raise exceptions.CommandSyntaxError(command=command)
