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


class ConfCommandProcessor(BaseCommandProcessor):
    def do_exit(self, command, *args, context=None):
        from .enaCommandProcessor import EnaCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = EnaCommandProcessor
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

    def do_interface(self, command, *args, context=None):
        if self._validate(args, str):
            ident, = self._dissect(args, str)
            if ident.startswith('GigaEthernet'):
                port = ident[12:]
                try:
                    port = self._model.get_port('name', port)
                except exceptions.SoftboxenError:
                    full_command = command
                    for arg in args:
                        full_command += ' ' + arg
                    context['full_command'] = full_command
                    raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                    ('login', 'mainloop', 'ena', 'conf'))

                from .interaceCommandProcessor import InterfaceCommandProcessor
                subprocessor = self._create_subprocessor(InterfaceCommandProcessor, 'login', 'mainloop', 'ena', 'conf',
                                                         'interface')
                context['component'] = port
                subprocessor.loop(context=context)

            else:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)