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
from datetime import datetime

from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class UserViewCommandProcessor(BaseCommandProcessor):

    def do_enable(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        subprocessor = self._create_subprocessor(
            EnableCommandProcessor, 'login', 'mainloop', 'enable')

        subprocessor.loop(context=context)

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_quit(self, command, *args, context=None):
        self._write("  Check whether system data has been changed. Please save data before logout.\n")
        answer = self.user_input("Are you sure to log out? (y/n)[n]:")
        if answer == "y":
            self._model.set_last_logout(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            exc = exceptions.TerminalExitError()
            exc.return_to = 'sysexit'
            raise exc
        return

    def on_help(self, command, args, context=None):
        if self._validate(command, 'help'):
            text = self._render(
                'help',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

