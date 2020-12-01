# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class EnaCommandProcessor(BaseCommandProcessor):
    def do_exit(self, command, *args, context=None):
        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_conf(self, command, *args, context=None):
        from .confCommandProcessor import ConfCommandProcessor
        if args == ():
                subprocessor = self._create_subprocessor(ConfCommandProcessor, 'login', 'mainloop', 'ena', 'conf')
                subprocessor.loop(context=context)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_show(self, command, *args, context=None):
        if self._validate(args, 'interface', 'gigaEthernet', str):
            port_name, = self._dissect(args, 'interface', 'gigaEthernet', str)

            try:
                port = self._model.get_port('name', port_name)
            except exceptions.SoftboxenError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                                                       ('login', 'mainloop', 'ena'))

            _, port_index = port.name.split('/')
            context['port_index'] = port_index
            self.map_states(port, 'port')
            text = self._render('show_interface_gigaEthernet_port', context=dict(context, port=port))
            self._write(text)

        elif self._validate(args, 'running-config', 'interface', 'gigaEthernet', str):
            port_name, = self._dissect(args, 'running-config', 'interface', 'gigaEthernet', str)

            try:
                port = self._model.get_port('name', port_name)
            except exceptions.SoftboxenError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                                                       ('login', 'mainloop', 'ena'))

            text = self._render('show_running-config_interface_gigaEthernet_port', context=dict(context, port=port))
            self._write(text)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)
