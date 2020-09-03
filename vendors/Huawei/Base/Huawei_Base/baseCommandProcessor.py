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
from nesi.softbox.cli import base


class BaseCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    VENDOR = 'Huawei'
    MODEL = 'Base'
    VERSION = '1'

    def user_input(self, prompt):
        self._write(prompt)
        prompt_end_pos = self.prompt_end_pos
        self.prompt_end_pos = len(prompt) - 1
        input = self._read().strip()
        self.prompt_end_pos = prompt_end_pos
        return input

    def do_quit(self, command, *args, context=None):
        raise exceptions.TerminalExitError()

    def do_undo(self, command, *args, context=None):      # TODO: Functionality
        if self._validate(args, 'alarm', 'output', 'all'):
            return
        elif self._validate(args, 'event', 'output', 'all'):
            return
        elif self._validate(args, 'smart'):
            return
        elif self._validate(args, 'system', 'snmp-user', 'password', 'security'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_scroll(self, command, *args, context=None):
        if args == ():
            _ = self.user_input('{ <cr>|number<U><10,512> }:')
            return
        elif self._validate(args, str):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def create_spacers(self, positions, args):
        spacers = []
        previous_pos = 0
        i = 0
        for position in positions:
            spacer = position - (previous_pos + len(str(args[i])))
            spacers.append(spacer)
            previous_pos = position
            i += 1

        return spacers

    def space_out_port_name(self, name):
        name_components = name.split('/')
        spaced_out_name = ''
        i = 0

        for component in name_components:
            spaced_out_name += ' ' + component
            i = i + 1
            if i != 3:
                spaced_out_name += '/'

        return spaced_out_name
