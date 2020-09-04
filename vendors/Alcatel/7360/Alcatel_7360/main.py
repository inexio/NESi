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

from nesi.softbox.cli import base
from nesi import exceptions
from datetime import datetime, date
from vendors.Alcatel.Base.Alcatel_Base.userViewCommandProcessor import UserViewCommandProcessor


class ReadInputCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    VENDOR = 'Alcatel'
    MODEL = '7360'
    VERSION = 'FX-4'


class PreLoginCommandProcessor(ReadInputCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            LoginCommandProcessor, 'login')

        context['username'] = context['raw_line']

        try:
            subprocessor.history_enabled = False
            subprocessor.hide_input = True
            subprocessor.loop(context=context)
        except exceptions.TerminalExitError as exc:
            if exc.return_to is not None and exc.return_to != 'sysexit':
                raise exc
            else:
                self.on_exit(context)
                raise exc


class LoginCommandProcessor(ReadInputCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        context['welcome_banner'] = self._model.welcome_banner
        username = context.pop('username')
        password = command

        for creds in self._model.credentials:
            if creds.username == username and creds.password == password:
                break

        else:
            text = self._render('password', context=context)
            self._write(text)
            raise exceptions.TerminalExitError()

        subprocessor = self._create_subprocessor(
            UserViewCommandProcessor, 'login', 'mainloop')

        context['timestamp'] = self._model.last_login
        context['meltStart'] = False
        context['session_id'] = ''

        self.on_exit(context)
        self._model.set_last_login(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        subprocessor.loop(context=context)
