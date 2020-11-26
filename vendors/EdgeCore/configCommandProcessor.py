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
import random
import datetime
import re
import time

from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class ConfigCommandProcessor(BaseCommandProcessor):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_interface(self, command, *args, context=None):
        if self._validate(args, 'ethernet', str):
            interface_name, = self._dissect(args, 'ethernet', str)

            try:
                _ = self._model.get_interface('name', interface_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            from .interfaceCommandProcessor import InterfaceCommandProcessor

            subprocessor = self._create_subprocessor(InterfaceCommandProcessor, 'login', 'mainloop', 'enable', 'config',
                                                     'interface')
            subprocessor.set_interface_name(interface_name)
            subprocessor.loop(return_to=ConfigCommandProcessor, context=dict(context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vlan(self, command, *args, context=None):
        if self._validate(args, 'database'):
            from .vlanCommandProcessor import VlanCommandProcessor

            subprocessor = self._create_subprocessor(VlanCommandProcessor, 'login', 'mainloop', 'enable', 'config',
                                                     'vlan')
            subprocessor.loop(return_to=ConfigCommandProcessor, context=dict(context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_no(self, command, *args, context=None):
        if self._validate(args, 'logging', 'host', str):
            host, = self._dissect(args,  'logging', 'host', str)
            box = self._model
            if host in box.logging_host:
                addresss = box.logging_host.split(', ')
                ports = box.logging_port.split(', ')
                index = 0
                for address in addresss:
                    if address == host:
                        break
                    index += 1
                addresss.remove(host)
                ports.pop(index)
                address_list = ', '.join(addresss)
                port_list = ', '.join(ports)
                box.set('logging_host', address_list)
                box.set('logging_port', port_list)
            else:
                pass
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_management(self, command, *args, context=None):
        if self._validate(args, 'all-client', str, str):
            start, end = self._dissect(args, 'all-client', str, str)
            box = self._model
            box.set('management_start_address', start)
            box.set('management_end_address', end)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_loopback_detection(self, command, *args, context=None):
        if self._validate(args, 'action', str):
            prop, = self._dissect(args,  'action', str)
            box = self._model
            box.set('loopback_detection_action', prop)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_sntp(self, command, *args, context=None):
        if self._validate(args, 'server', str):
            ip, = self._dissect(args, 'server', str)
            box = self._model
            box.set('sntp_server_ip', ip)
        elif self._validate(args, 'client'):
            box = self._model
            box.set('sntp_client', 'Enabled')
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_clock(self, command, *args, context=None):
        if self._validate(args, 'timezone', str, 'hours', str, 'minute', str):
            name, h, m = self._dissect(args, 'timezone', str, 'hours', str, 'minute', str)
            box = self._model
            box.set('timezone_name', name)
            box.set('timezone_time', (h + ',' + m))
        elif self._validate(args, 'summer-time', str, 'predefined', str):
            name, region = self._dissect(args, 'summer-time', str, 'predefined', str)
            box = self._model
            box.set('summer_time_name', name)
            box.set('summer_time_region', region)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_prompt(self, command, *args, context=None):
        if self._validate(args, str):
            name, = self._dissect(args, str)
            box = self._model
            box.set('hostname', name)
            self.set_prompt_end_pos(context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_hostname(self, command, *args, context=None):
        if self._validate(args, str):
            name, = self._dissect(args, str)
            box = self._model
            box.set('hostname', name)
            self.set_prompt_end_pos(context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_logging(self, command, *args, context=None):
        if self._validate(args, 'host', str, 'port', str):
            host, port = self._dissect(args, 'host', str, 'port', str)
            box = self._model
            if host not in box.logging_host:
                address_list = box.logging_host + ', ' + host
                port_list = box.logging_port + ', ' + port
                box.set('logging_host', address_list)
                box.set('logging_port', port_list)

        elif self._validate(args, 'trap'):
            box = self._model
            box.set('logging_level', 7)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ip(self, command, *args, context=None):
        if self._validate(args, 'dhcp', 'snooping'):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'vlan', str):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'information', 'option', 'encode', 'no-subtype'):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'information', 'option', 'remote-id', 'string', str, 'sub-option',
                            'port-description'):
            pass             # No visible changes

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pppoe(self, command, *args, context=None):
        if self._validate(args, 'intermediate-agent'):
            pass             # No visible changes

        else:
            raise exceptions.CommandSyntaxError(command=command)

