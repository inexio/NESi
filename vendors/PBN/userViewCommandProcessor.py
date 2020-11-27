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


class UserViewCommandProcessor(BaseCommandProcessor):

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

    def do_ena(self, command, *args, context=None):
        from .enaCommandProcessor import EnaCommandProcessor

        if args == ():
            self.hide_input = True
            password = self.user_input('password:', False)
            try:
                creds = self._model.get_credentials('username', 'ena')
                assert creds.password == password
            except (exceptions.SoftboxenError, AssertionError):
                text = self._render('ena_error', context=context)
                self._write(text)
            else:
                self.hide_input = False
                subprocessor = self._create_subprocessor(EnaCommandProcessor, 'login', 'mainloop', 'ena')
                subprocessor.loop(context=context)

        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)
