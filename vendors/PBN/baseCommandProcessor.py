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
from nesi.softbox.cli import base


class BaseCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    def do_exit(self, command, *args, context=None):
        user = self._model.get_user('status', 'online')
        user.set_offline()
        raise exceptions.TerminalExitError()

    def on_unknown_command(self, command, *args, context=None):
        full_command = command
        for arg in args:
            full_command += ' ' + arg
        context['full_command'] = full_command
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

    def user_input(self, prompt, allow_history=True, tmp_boundary=None):
        self._write(prompt)
        prompt_end_pos = self.prompt_end_pos
        self.prompt_end_pos = len(prompt) - 1
        if not allow_history:
            self.history_enabled = False

        if len(self.line_buffer) != 0:
            input = self.line_buffer.pop(0)
        else:
            input = self._read(tmp_boundary).strip()
        if not allow_history:
            self.history_enabled = True
        self.prompt_end_pos = prompt_end_pos
        return input

    def map_states(self, object, type):
        if object.admin_state == '0':
            if type == 'port':
                object.admin_state = 'down'
            elif type == 'ont_port':
                object.admin_state = 'Down'
        elif object.admin_state == '1':
            if type == 'port':
                object.admin_state = 'up'
            elif type == 'ont_port':
                object.admin_state = 'Up'

        if object.operational_state == '0':
            if type == 'port':
                object.operational_state = 'down'
            elif type == 'ont_port':
                object.operational_state = 'Link-Down'
        elif object.operational_state == '1':
            if type == 'port':
                object.operational_state = 'up'
            elif type == 'ont_port':
                object.operational_state = 'Link-Up'
