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
from .baseMixIn import BaseMixIn


class DiagnoseCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def do_disable(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def do_return(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = EnableCommandProcessor
        raise exc

    def do_system(self, command, *args, context=None):
        if self._validate(args, 'status', 'collect', 'all'):
            box = self._model
            result = ['Abnormal', 'Normal'][int(box.cpu_occupancy[:-1]) <= 80]
            context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
            text = self._render('display_system_status_collection', context=dict(context, box=box, result=result))
            for card in self._model.cards:
                result = ['Abnormal', 'Normal'][card.board_status == 'Normal' or card.board_status == 'Active_normal']
                context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                text += self._render('display_system_status_collection_1',
                                     context=dict(context, card=card, result=result))
            text += self._render('display_system_status_collection_2', context=context)
            text2 = ''
            for subrack in self._model.subracks:
                result = ['Abnormal', 'Normal'][subrack.frame_status == 'active']
                context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                text += self._render('display_system_status_collection_3',
                                     context=dict(context, subrack=subrack, result=result))
                result = ['Abnormal', 'Normal'][int(subrack.temperature[:-1]) <= 80]
                context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                text2 += self._render('display_system_status_collection_4',
                                      context=dict(context, subrack=subrack, result=result))

            text += self._render('display_system_status_collection_2', context=context)
            text += text2
            text += self._render('display_system_status_collection_5', context=context)
            text2 = ''
            for emu in self._model.emus:
                if emu.type == 'FAN':
                    result = ['Abnormal', 'Normal'][emu.emu_state == 'Normal']
                    context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                    text += self._render('display_system_status_collection_6',
                                         context=dict(context, emu=emu, result=result))
                else:
                    result = ['Abnormal', 'Normal'][emu.emu_state == 'Normal']
                    context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                    text2 += self._render('display_system_status_collection_9',
                                          context=dict(context, emu=emu, result=result))
            text += self._render('display_system_status_collection_7', context=context)
            for port in self._model.ports:
                result = ['Abnormal', 'Normal'][port.admin_state == 'activated']
                context['spacer'] = self.create_spacers((9,), (result,))[0] * ' '
                text += self._render('display_system_status_collection_8',
                                     context=dict(context, port=port, result=result))
            text += self._render('display_system_status_collection_5', context=context)
            text += text2
            text += self._render('display_system_status_collection_10',
                                 context=dict(context, time=datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
            context['text'] = text
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_display(self, command, *args, context=None):
        if self._validate(args, 'system', 'status', 'collection'):
            try:
                text = context['text']
            except KeyError:
                raise exceptions.CommandSyntaxError(command=command)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_switch(self, command, *args, context=None):  # TODO: Functionality (that isn't how the switch command works)
        if self._validate(args, 'vdsl', 'mode', 'to', str):
            aone = self.user_input('Please enter y if you want to continue: ')
            if aone != 'y':
                raise exceptions.InvalidInputError
            atwo = self.user_input('Please enter y again to confirm: ')
            if atwo != 'y':
                raise exceptions.InvalidInputError
        else:
            raise exceptions.CommandSyntaxError(command=command)
