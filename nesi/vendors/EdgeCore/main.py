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

from nesi.devices.softbox.cli import base
from vendors.EdgeCore.userViewCommandProcessor import *
from nesi import exceptions


class PreLoginCommandProcessor(base.CommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            LoginCommandProcessor, 'login')

        context['username'] = context['raw_line'].replace('\r', '').replace('\n', '')

        try:
            subprocessor.history_enabled = False
            subprocessor.hide_input = True
            context['ip'] = self._model.network_address
            context['name'] = self._model.hostname
            subprocessor.loop(context=context)
        except exceptions.TerminalExitError as exc:
            if exc.return_to is not None and exc.return_to != 'sysexit':
                raise exc
            else:
                context['ip'] = self._model.network_address
                self.on_exit(context)
                raise exc


class LoginCommandProcessor(base.CommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        username = context.pop('username')
        password = command

        for creds in self._model.credentials:
            if creds.username == username and creds.password == password:
                user = self._model.get_user('id', creds.user_id)
                if user.profile == 'root':
                    break
        else:
            text = self._render('password', context=context)
            self._write(text)
            raise exceptions.TerminalExitError()

        self._output.write(bytes(False))
        self._output.write(bytes(False))

        subprocessor = self._create_subprocessor(
            UserViewCommandProcessor, 'login', 'mainloop')

        subprocessor.loop(context=context)


class PostLoginCommandProcessor(base.CommandProcessor):

    def loop(self, context=None, return_to=None, command=None):
        subprocessor = self._create_subprocessor(
            UserViewCommandProcessor, 'login', 'mainloop')

        subprocessor.loop(context=context)
