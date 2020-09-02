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


class TestCommandProcessor(BaseCommandProcessor):

    def do_return(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = EnableCommandProcessor
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_xdsl(self, command, *args, context=None):
        if self._validate(args, 'melt', str, 'measured-frequency', '25Hz', 'busy', 'force'):
            port_idx, = self._dissect(args, 'melt', str, 'measured-frequency', '25Hz', 'busy', 'force')

            try:
                port = self._model.get_port('name', port_idx)
                card = self._model.get_card('id', port.card_id)
                assert (card.product == 'xdsl') or (card.product == 'adsl') or (card.product == 'vdsl')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            _ = self.user_input('{ <cr>|discharge<K>|fault-force-test<K> }:')

            text = self._render('melt_failure', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)
