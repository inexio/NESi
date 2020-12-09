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
from nesi.softbox.cli import base


class BaseCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    def do_exit(self, command, *args, context=None):
        raise exceptions.TerminalExitError()

    def do_logout(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def on_unknown_command(self, command, *args, context=None):
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

    def fill_mau_template_context(self, mau, context):
        context['mau'] = mau

        i = 1

        spacers = self.create_spacers((25, 50, 75), (context['if_index'], mau.index, mau.type, mau.media_available))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((18, 35, 62),
                                      (mau.jabber_state, mau.b100basefxfd, mau.b100baselx10, mau.b100basebx10d))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((18, 35, 64),
                                      (mau.b100basebx10u, mau.b100basetxfd, mau.b1000basetfd, mau.b10gbasetfd))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((17, 33, 59),
                                      (mau.b1000basesxfd, mau.b1000baselx10, mau.b1000baselxfd, mau.b1000basebx10u))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((21, 40, 70), (mau.b1000basebx10d, mau.b10gbaser, mau.b10gbaselr, mau.b10gbaseer))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((12, 26, 52),
                                      (mau.b2500basex, mau.auto_neg_supported, mau.auto_neg_status, mau.cap100base_tfd))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

        spacers = self.create_spacers((15, 30), (mau.cap1000base_xfd, mau.cap1000base_tfd, mau.cap10gbase_tfd))
        for spacer in spacers:
            context['spacer' + str(i)] = spacer * ' '
            i += 1

    def name_joiner(self, args):
        saved_args = []
        save = False
        for i in range(len(args)):
            if args[i].startswith("\""):
                save = True
            if save:
                saved_args.append(args[i])
            if args[i].endswith("\""):
                save = False
        name = ' '.join(saved_args).replace("\"", "")

        return name

    def command_port_check(self, command, port_identifier):
        try:
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            assert (command == 'adsl' or command == 'vdsl' or command == 'xdsl' or command == 'sdsl')
            assert (card.product == command)
        except (exceptions.SoftboxenError, AssertionError):
            raise exceptions.CommandSyntaxError(command=command)

        return port
