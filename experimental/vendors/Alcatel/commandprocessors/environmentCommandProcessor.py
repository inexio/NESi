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
from .baseMixIn import BaseMixIn


class EnvironmentCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_inhibit_alarms(self, command, *args, context=None):
        if self._validate(args, '?'):
            text = self._render('inhibit_alarms_help', context=context)
            self._write(text)
        elif self._validate(args, 'mode', '?'):
            text = self._render('inhibit_alarms_mode_help', context=context)
            self._write(text)
        elif self._validate(args, 'mode', 'batch', '?'):
            text = self._render('inhibit_alarms_mode_batch_help', context=context)
            self._write(text)
        elif self._validate(args, 'mode', 'batch', 'print', '?'):
            text = self._render('inhibit_alarms_mode_batch_print_help', context=context)
            self._write(text)
        elif self._validate(args, 'mode', 'batch', 'print', 'no-more', '?'):
            text = self._render('inhibit_alarms_mode_batch_print_no_more_help', context=context)
            self._write(text)
        elif self._validate(args, 'mode', 'batch', 'print', 'no-more'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)
