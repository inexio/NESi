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

from nesi.softbox.cli import base
from vendors.Huawei.Base.Huawei_Base.userViewCommandProcessor import *
from nesi import exceptions


class ReadInputCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    VENDOR = 'Huawei'
    MODEL = '5623'
    VERSION = 'A'


class PreLoginCommandProcessor(ReadInputCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        subprocessor = self._create_subprocessor(
            LoginCommandProcessor, 'login')

        context['username'] = command

        try:
            subprocessor.loop(context=context)
        except exceptions.TerminalExitError as exc:
            if exc.return_to is not None and exc.return_to != 'sysexit':
                raise exc
            else:
                self.on_exit(context)
                raise exc


class LoginCommandProcessor(ReadInputCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        username = context.pop('username')
        password = command

        for creds in self._model.credentials:
            if creds.username == username and creds.password == password:
                user = self._model.get_user('credentials_id', creds.id)
                if user.lock_status == 'Locked':
                    text = self._render('user_locked', context=context)
                    self._write(text)
                    raise exceptions.TerminalExitError()
                num = user.reenter_num
                user.set_reenter_num_temp(num)
                user.set_online()
                break

        else:
            try:
                user = self._model.get_user('name', username)
            except exceptions.SoftboxenError:
                text = self._render('password', context=context)
                self._write(text)
                raise exceptions.TerminalExitError()
            else:
                if user.reenter_num_temp < 0:
                    if user.level == 'Admin':
                        user.set_reenter_num_temp(user.reenter_num)
                        text = self._render('password', context=context)
                        self._write(text)
                        raise exceptions.TerminalExitError()
                    else:
                        user.lock()
                        text = self._render('user_locked', context=context)
                        self._write(text)
                        raise exceptions.TerminalExitError()
                else:
                    num = user.reenter_num_temp - 1
                    user.set_reenter_num_temp(num)
                    text = self._render('password', context=context)
                    self._write(text)
                    raise exceptions.TerminalExitError()

        self._output.write(bytes(False))
        self._output.write(bytes(False))

        subprocessor = self._create_subprocessor(
            UserViewCommandProcessor, 'login', 'mainloop')

        context['timestamp1'] = self._model.last_login
        context['timestamp2'] = self._model.last_logout
        self._model.set_last_login(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        self._model.set_last_logout('/')

        subprocessor.loop(context=context)
