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

        for i in range(0, 3):
            self.hide_input = True
            enable_pw = self.user_input("Password:", False, None)
            self.hide_input = False

            for creds in self._model.credentials:
                if creds.username == 'enable':
                    user = self._model.get_user('id', creds.user_id)
                    if user.profile == 'enable':
                        break

            if creds.password == enable_pw:
                break
        else:
            text = self._render('enable_password', context=context)
            self._write(text)
            return

        from .enableCommandProcessor import EnableCommandProcessor

        subprocessor = self._create_subprocessor(
            EnableCommandProcessor, 'login', 'mainloop', 'enable')

        subprocessor.loop(context=context)

    def do_disable(self, command, *args, context=None):
        return

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def on_help(self, command, *args, context=None):
        if args == ():
            text = self._render(
                'help',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)
