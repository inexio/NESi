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

import time


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
                result = ['Abnormal', 'Normal'][port.admin_state == '1']
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

    def do_switch(self, command, *args, context=None):
        if self._validate(args, 'vdsl', 'mode', 'to', str):
            user = self._model.get_user('status', 'online')
            if user.level != 'Super':
                raise exceptions.CommandSyntaxError(command=command)

            dsl_mode, = self._dissect(args, 'vdsl', 'mode', 'to', str)
            context['dsl_mode'] = dsl_mode
            if dsl_mode != 'tr129' and dsl_mode != 'tr165':
                self.line_buffer = []
                raise exceptions.CommandSyntaxError(command=command)

            if self._model.smart_mode:
                self.user_input('{ <cr>|adsl<K> }:', False)
                text = self._render('switch_dsl_mode_temp_1', context=context)
                self._write(text)

            if self._model.dsl_mode == dsl_mode:
                text = self._render('switch_dsl_mode_failure', context=context)
                self._write(text)
                self.line_buffer = []
                return

            answer_one = 'y'
            if self._model.interactive_mode:
                answer_one = self.user_input('  Warning: The operation will result in loss of all VDSL configuration. '
                                             'Are you sure to proceed? (y/n)[n]:', False)
            if answer_one != 'y':
                self.line_buffer = []
                return

            answer_two = 'y'
            if self._model.interactive_mode:
                answer_two = self.user_input('  Warning: The operation will automatically save and reboot system. '
                                             'Are you sure you want to proceed? (y/n)[n]:', False)
            if answer_two != 'y':
                self.line_buffer = []
                return

            text = self._render('switch_dsl_mode_temp_2', context=context)
            self._write(text)
            self._model.set_dsl_mode(dsl_mode)
            self.on_cycle(context=context)

            mgmt_card = self._model.get_card('product', 'mgnt')
            context['mgmt_card'] = mgmt_card.name[2:]
            x = 6
            while x <= 100:
                time.sleep(1)
                context['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                context['progress'] = x
                self._write(self._render('saving_progress', context=context))
                self.on_cycle(context=context)
                x += 6

            context['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._write(self._render('saving_complete', context=context))
            self.on_cycle(context=context)
            time.sleep(10)
            self._model.set_last_logout(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            user = self._model.get_user('status', 'online')
            user.set_offline()
            exc = exceptions.TerminalExitError()
            exc.return_to = 'sysreboot'
            raise exc

        else:
            raise exceptions.CommandSyntaxError(command=command)
