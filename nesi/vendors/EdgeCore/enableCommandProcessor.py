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
import time


class EnableCommandProcessor(BaseCommandProcessor):

    def do_disable(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if command == '?' and args == ():
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_configure(self, command, *args, context=None):

        from .configCommandProcessor import ConfigCommandProcessor

        subprocessor = self._create_subprocessor(
            ConfigCommandProcessor, 'login', 'mainloop', 'enable', 'config')

        subprocessor.loop(context=context, return_to=EnableCommandProcessor)

    def do_config(self, command, *args, context=None):

        from .configCommandProcessor import ConfigCommandProcessor

        subprocessor = self._create_subprocessor(
            ConfigCommandProcessor, 'login', 'mainloop', 'enable', 'config')

        subprocessor.loop(context=context, return_to=EnableCommandProcessor)

    def do_show(self, command, *args, context=None):
        if command == '?' and args == ():
            text = self._render('show_?', context=context)
            self._write(text)
        elif self._validate(args, 'interfaces', 'status', 'ethernet', str):
            port_name, = self._dissect(args, 'interfaces', 'status', 'ethernet', str)
            try:
                port = self._model.get_port('name', port_name)
                self.map_states(port, 'port')
                interface = self._model.get_interface('name', port_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            # TODO: Information of Interface
            text = self._render('show_interface_status', context=dict(context, port=port, interface=interface))
            self._write(text)
        elif self._validate(args, 'interfaces', 'switchport', 'ethernet', str):
            port_name, = self._dissect(args, 'interfaces', 'switchport', 'ethernet', str)
            try:
                port = self._model.get_port('name', port_name)
                self.map_states(port, 'port')
                interface = self._model.get_interface('name', port_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            # TODO: Information of Interface
            text = self._render('show_interface_switchport', context=dict(context, port=port, interface=interface))
            self._write(text)
        elif self._validate(args, 'interfaces', 'transceiver', 'ethernet', str):
            port_name, = self._dissect(args, 'interfaces', 'transceiver', 'ethernet', str)
            try:
                port = self._model.get_port('name', port_name)
                self.map_states(port, 'port')
                interface = self._model.get_interface('name', port_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            # TODO: Information of Interface
            # erst ab port 25-28
            text = self._render('show_interface_transceiver', context=dict(context, port=port, interface=interface))
            self._write(text)
        elif self._validate(args, 'system'):
            try:
                card = self._model.get_card('name', "1")
                self.map_states(card, 'card')
                box = self._model
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            text = self._render('show_system', context=dict(context, card=card, box=box))
            self._write(text)
        elif self._validate(args, 'process', 'cpu'):
            text = self._render('show_process_cpu', context=context)
            self._write(text)
        elif self._validate(args, 'memory'):
            text = self._render('show_memory', context=context)
            self._write(text)
        elif self._validate(args, 'mac-address-table'):
            text = self._render('show_mac_address_table', context=context)
            for interface in self._model.interfaces:
                text += self._render('show_mac_address_table_entry', context=dict(context, interface=interface))
            card = self._model.get_card('name', "1")
            self.map_states(card, 'card')
            text += self._render('show_mac_address_table_unit', context=dict(context, card=card))
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_copy(self, command, *args, context=None):
        if self._validate(args, 'startup-config', 'ftp'): # Work in progess
            ip = self.user_input("FTP server IP address: ", False, None)
            user = self.user_input("User [Anonymous]: ", False, None)
            self.hide_input = True
            pw = self.user_input("Password: ", False, None)
            self.hide_input = False
            dest = self.user_input("Destination file name: ", False, None)

            for creds in self._model.credentials:
                if creds.username == user:
                    user = self._model.get_user('id', creds.user_id)
                    if user.profile == 'backup':
                        break

            if creds.password != pw or '/' not in dest or ip.count('.') != 3:
                text = self._render('copy_startup_config_ftp_failure', context=context)
                self._write(text)
            else:
                text = self._render('copy_startup_config_ftp_success', context=context)
                self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_help(self, command, *args, context=None):
        if args == ():
            text = self._render(
                'help',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)
