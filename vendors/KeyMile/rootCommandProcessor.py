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
from .baseCommandProcessor import BaseCommandProcessor
from .changeDirectoryProcessor import ChangeDirectoryProcessor


class RootCommandProcessor(BaseCommandProcessor, ChangeDirectoryProcessor):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_help(self, command, *args, context=None):
        if self._validate(args, str):
            help_arg, = self._dissect(args, str)

            if help_arg == 'cd':
                self._write(self._render('help_cd', context=context))
            elif help_arg == 'pwd':
                self._write(self._render('help_pwd', context=context))
            elif help_arg == 'ls':
                self._write(self._render('help_ls', context=context))
            elif help_arg == 'show':
                self._write(self._render('help_show', context=context))
            elif help_arg == 'mode':
                self._write(self._render('help_mode', context=context))
            elif help_arg == 'ftpserver':
                self._write(self._render('help_ftpserver', context=context))
            elif help_arg == 'upload':
                self._write(self._render('help_upload', context=context))
            elif help_arg == 'download':
                self._write(self._render('help_download', context=context))
            elif help_arg == 'get':
                self._write(self._render('help_get', context=context))
            elif help_arg == 'set':
                self._write(self._render('help_set', context=context))
            elif help_arg == 'profile':
                self._write(self._render('help_profile', context=context))
            elif help_arg == 'help':
                self._write(self._render('help_help', context=context))
            elif help_arg == 'exit':
                self._write(self._render('help_exit', context=context))
            else:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args,):
            self._write(self._render('help', context=context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def do_ls(self, command, *args, context=None):
        if self._validate(args,):
            text = self._render('ls_header', context=context)

            for card in self._model.cards:
                text += self._render('ls_body', context=dict(context, card=card))

            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)