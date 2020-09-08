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

    def map_states(self, object, type):
        if object.admin_state == '0':
            if type == 'subrack':
                object.admin_state = 'lock'
            elif type in ('card', 'port', 'ont_port'):
                object.admin_state = 'deactivated'
            elif type == 'service_port':
                object.admin_state = 'disable'
            elif type in ('ont', 'ont_port', 'cpe'):
                object.admin_state = 'offline'
        elif object.admin_state == '1':
            if type == 'subrack':
                object.admin_state = 'unlock'
            elif type in ('card', 'port', 'ont_port'):
                object.admin_state = 'activated'
            elif type == 'service_port':
                object.admin_state = 'enable'
            elif type in ('ont', 'ont_port', 'cpe'):
                object.admin_state = 'online'
        elif object.admin_state == '2':
            if type == 'port':
                object.admin_state = 'activating'

        if object.operational_state == '0':
            if type in ('subrack', 'card'):
                object.operational_state = 'disabled'
            elif type == 'port':
                object.operational_state = 'deactivated'
            elif type == 'service_port':
                object.operational_state = 'down'
            elif type in ('ont', 'ont_port'):
                object.operational_state = 'offline'
        elif object.operational_state == '1':
            if type in ('subrack', 'card'):
                object.operational_state = 'enabled'
            elif type == 'port':
                object.operational_state = 'activated'
            elif type == 'service_port':
                object.operational_state = 'up'
            elif type in ('ont', 'ont_port'):
                object.operational_state = 'online'
        elif object.operational_state == '2':
            if type in ('port', 'ont_port'):
                object.operational_state = 'activating'

    def user_input(self, prompt, allow_history=True, tmp_boundary=None):
        self._write(prompt)
        prompt_end_pos = self.prompt_end_pos
        self.prompt_end_pos = len(prompt) - 1
        if not allow_history:
            self.history_enabled = False
        input = self._read(tmp_boundary).strip()
        if not allow_history:
            self.history_enabled = True
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
