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
from .huaweiBaseCommandProcessor import HuaweiBaseCommandProcessor
import time


class EnableCommandProcessor(HuaweiBaseCommandProcessor):

    def do_disable(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def do_quit(self, command, *args, context=None):
        self._write("  Check whether system data has been changed. Please save data before logout.\n")
        answer = self.user_input("Are you sure to log out? (y/n)[n]:")
        if answer == "y":
            self._model.set_last_logout(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            user = self._model.get_user('status', 'Online')
            user.set_offline()
            exc = exceptions.TerminalExitError()
            exc.return_to = 'sysexit'
            raise exc
        return

    def on_unknown_command(self, command, *args, context=None):
        if command == '?' and args == ():
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_config(self, command, *args, context=None):

        from .configCommandProcessor import ConfigCommandProcessor

        try:
            admin = self._model.get_user('status', 'Online')
            assert admin.level != 'User'
        except (exceptions.SoftboxenError, AssertionError):
            raise exceptions.CommandSyntaxError(command=command)

        subprocessor = self._create_subprocessor(
            ConfigCommandProcessor, 'login', 'mainloop', 'enable', 'config')

        subprocessor.loop(context=context, return_to=EnableCommandProcessor)

    def do_diagnose(self, command, *args, context=None):

        from .diagnoseCommandProcessor import DiagnoseCommandProcessor

        subprocessor = self._create_subprocessor(
            DiagnoseCommandProcessor, 'login', 'mainloop', 'enable', 'diagnose')

        subprocessor.loop(context=context, return_to=EnableCommandProcessor)

    def do_display(self, command, *args, context=None):
        if self._validate(args, 'interface', str, str):
            # TODO: dynamic profile output
            product, port_identifier = self._dissect(args, 'interface', str, str)

            try:
                port = self._model.get_port("name", port_identifier)
                self.map_states(port, 'port')
                card = self._model.get_card('id', port.card_id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product != product:
                raise exceptions.CommandSyntaxError(command=command)

            context['spaced_out_name'] = self.space_out_port_name(port.name)
            context['spacer'] = self.create_spacers((7,), (port.dynamic_profile_index,))[0] * ' '

            try:
                service_port = self._model.get_service_port('connected_id', port.id)
            except exceptions.SoftboxenError:
                context['vlan_fields'] = False
            else:
                context['vlan_fields'] = True
                try:
                    service_vlan = self._model.get_service_vlan('service_port_id', service_port.id)
                    vlan = self._model.get_vlan('id', service_vlan.vlan_id)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                context['s_port'] = service_port
                context['vlan'] = vlan
            text = self._render(
                'display_interface_product_port',
                context=dict(context, port=port, card=card))
            self._write(text)
        elif self._validate(args, 'temperature', str):
            card_identifier, = self._dissect(args, 'temperature', str)
            try:
                card = self._model.get_card('name', card_identifier)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['f'] = int(int(card.temperature[:-1]) * 9/5 + 32)
            text = self._render('display_temperature', context=dict(context, card=card))
            self._write(text)
        elif self._validate(args, str, 'port', 'state', str):
            product, port_identifier = self._dissect(args, str, 'port', 'state', str)

            try:
                port = self._model.get_port("name", port_identifier)
                self.map_states(port, 'port')
                card = self._model.get_card('id', port.card_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product != product:
                raise exceptions.CommandSyntaxError(command=command)

            _, _, portname = port_identifier.split('/')
            channelname = portname + '.1'
            context['portname'] = portname
            context['channelname'] = channelname

            text = ''
            if port.admin_state == '1':
                context['spacer1'] = self.create_spacers((7,), (portname,))[0] * ' '
                context['spacer2'] = self.create_spacers((15,), (port.admin_state,))[0] * ' '
                context['spacer3'] = self.create_spacers((25,), (port.loopback,))[0] * ' '
                context['spacer4'] = self.create_spacers((14,), (port.alarm_template_num,))[0] * ' '
                context['spacer5'] = self.create_spacers((13,), (port.spectrum_profile_num,))[0] * ' '
                context['spacer6'] = self.create_spacers((17,), (portname,))[0] * ' '
                context['spacer7'] = self.create_spacers((14,), (port.dpbo_profile_num,))[0] * ' '
                context['spacer8'] = self.create_spacers((14,), (port.rfi_profile_num,))[0] * ' '
                context['spacer9'] = self.create_spacers((13,), (port.noise_margin_profile_num,))[0] * ' '
                context['spacer10'] = self.create_spacers((12,), (port.virtual_noise_profile_num,))[0] * ' '
                context['spacer11'] = self.create_spacers((18,), (channelname,))[0] * ' '
                context['spacer12'] = self.create_spacers((13,), (port.channel_ds_data_rate_profile_num,))[0] * ' '
                context['spacer13'] = self.create_spacers((13,), (port.channel_us_data_rate_profile_num,))[0] * ' '
                context['spacer14'] = self.create_spacers((11,), (port.channel_inp_data_rate_profile_num,))[0] * ' '
                context['spacer15'] = self.create_spacers((15,), (port.channel_ds_rate_adapt_ratio,))[0] * ' '
                text = self._render(
                    'display_product_port_state_num_card_port_activated',
                    context=dict(context, port=port))
            else:
                context['spacer1'] = self.create_spacers((7,), (portname,))[0] * ' '
                context['spacer2'] = self.create_spacers((14,), (port.admin_state,))[0] * ' '
                context['spacer3'] = self.create_spacers((16,), (port.loopback,))[0] * ' '
                context['spacer4'] = self.create_spacers((15,), (port.alarm_template_num,))[0] * ' '
                context['spacer5'] = self.create_spacers((19,), (port.spectrum_profile_num,))[0] * ' '
                text = self._render(
                    'display_product_port_state_num_card_port_deactivated',
                    context=dict(context, port=port))

            self._write(text)

        elif self._validate(args, 'vdsl', 'line', 'operation', 'port', str):
            port_identifier, = self._dissect(
                args, 'vdsl', 'line', 'operation', 'port', str)

            try:
                port = self._model.get_port("name", port_identifier)
                card = self._model.get_card('id', port.card_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product != 'vdsl':
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render(
                'display_vdsl_line_operation_port_num_card_port',
                context=dict(context, port=port))
            self._write(text)

        elif self._validate(args, 'adsl', 'line', 'operation', 'port', str):
            port_identifier, = self._dissect(
                args, 'adsl', 'line', 'operation', 'port', str)

            try:
                port = self._model.get_port("name", port_identifier)
                card = self._model.get_card('id', port.card_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product != 'adsl':
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render(
                'display_adsl_line_operation_port_num_card_port',
                context=dict(context, port=port))
            self._write(text)

        elif self._validate(args, 'service-port', str):
            self.display_service_port(command, args, context)

        elif self._validate(args, 'board', str):
            self.display_board(command, args, context)
        elif self._validate(args, 'vdsl', 'line-profile', str):
            profile, = self._dissect(args, 'vdsl', 'line-profile', str)
            context['profile_id'] = profile
            text = self._render(
                'display_vdsl_line-profile_num',
                context=context)
            self._write(text)

        elif self._validate(args, 'terminal', 'user', 'all'):
            self.display_terminal_user(command, context)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_save(self, command, *args, context=None):
        if args == ():
            # all data are stored directly into the database
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_reboot(self, command, *args, context=None):
        if self._validate(args, 'system'):
            time.sleep(10)
            self._model.set_last_logout(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            user = self._model.get_user('status', 'Online')
            user.set_offline()
            exc = exceptions.TerminalExitError()
            exc.return_to = 'sysreboot'
            raise exc
        else:
            raise exceptions.CommandSyntaxError(command=command)
