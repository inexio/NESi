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
import re
from datetime import datetime, date
from ipaddress import IPv4Network
from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class InterfaceCommandProcessor(BaseCommandProcessor):

    component_name = None

    def set_interface_name(self, name):
        self.component_name = name

    def get_actual_interface(self, command):
        if self.component_name is None:
            raise exceptions.CommandExecutionError(command='Component name is None')
        try:
            return self._model.get_interface('name', self.component_name)
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

    def get_actual_port(self, command):
        if self.component_name is None:
            raise exceptions.CommandExecutionError(command='Component name is None')
        try:
            return self._model.get_port('name', self.component_name)
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shutdown(self, command, *args, context=None):
        if len(args) == 0:
            port = self.get_actual_port(command)
            port.admin_down()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_no(self, command, *args, context=None):
        if self._validate(args, 'shutdown'):
            port = self.get_actual_port(command)
            port.admin_up()

        elif self._validate(args, 'rate-limit', 'input'):
            interface = self.get_actual_interface(command)
            interface.set('ingress_state', 'Disabled')

        elif self._validate(args, 'rate-limit', 'output'):
            interface = self.get_actual_interface(command)
            interface.set('egress_state', 'Disabled')

        elif self._validate(args, 'description'):
            port = self.get_actual_port(command)
            port.set('description', '')

        elif self._validate(args, 'switchport', 'mode'):
            interface = self.get_actual_interface(command)
            interface.set('vlan_membership_mode', 'Hybrid')
            interface.set('native_vlan', 1)

        elif self._validate(args, 'switchport', 'native', 'vlan'):
            interface = self.get_actual_interface(command)
            interface.set('native_vlan', 1)

        elif self._validate(args, 'switchport', 'allowed', 'vlan'):
            interface = self.get_actual_interface(command)
            interface.set('allowed_vlan', '1(u)')

        elif self._validate(args, 'pppoe', 'intermediate-agent', 'port-enable'):
            pass             # No visible changes

        elif self._validate(args, 'pppoe', 'intermediate-agent', 'port-format-type', 'circuit-id'):
            pass             # No visible changes

        elif self._validate(args, 'ip', 'dhcp', 'snooping', 'information', 'option', 'circuit-id', 'tr101',
                            'no-vlan-field'):
            pass             # No visible changes

        elif self._validate(args, 'ip', 'dhcp', 'snooping', 'information', 'option', 'circuit-id'):
            pass             # No visible changes

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_rate_limit(self, command, *args, context=None):
        if self._validate(args, 'input', str):
            rate, = self._dissect(args, 'input', str)
            interface = self.get_actual_interface(command)
            interface.set('ingress_state', 'Enabled')
            interface.set('ingress_rate', int(rate))
        elif self._validate(args, 'output', str):
            rate, = self._dissect(args, 'output', str)
            interface = self.get_actual_interface(command)
            interface.set('egress_state', 'Enabled')
            interface.set('egress_rate', int(rate))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_description(self, command, *args, context=None):
        if self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_actual_port(command)
            port.set('description', descr)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_switchport(self, command, *args, context=None):
        if self._validate(args, 'mode', 'hybrid'):
            interface = self.get_actual_interface(command)
            interface.set('vlan_membership_mode', 'Hybrid')

        elif self._validate(args, 'mode', 'access'):
            interface = self.get_actual_interface(command)
            interface.set('vlan_membership_mode', 'Access')

        elif self._validate(args, 'mode', 'trunk'):
            interface = self.get_actual_interface(command)
            interface.set('vlan_membership_mode', 'Trunk')

        elif self._validate(args, 'allowed', 'vlan', 'add', str, 'tagged'):
            interface = self.get_actual_interface(command)
            id_list, = self._dissect(args, 'allowed', 'vlan', 'add', str, 'tagged')
            if ',' in id_list:
                ids = id_list.split(',')
                for id in ids:
                    try:
                        id = int(id)
                        _ = self._model.get_vlan('number', id)
                    except Exception:
                        raise exceptions.CommandSyntaxError(command=command)
            else:
                try:
                    id = int(id_list)
                    _ = self._model.get_vlan('number', id)
                except Exception:
                    raise exceptions.CommandSyntaxError(command=command)
            id_list = id_list + '(t)'
            interface.set('allowed_vlan', id_list)

        elif self._validate(args, 'allowed', 'vlan', 'add', str, 'untagged'):
            interface = self.get_actual_interface(command)
            id_list, = self._dissect(args, 'allowed', 'vlan', 'add', str, 'untagged')
            if ',' in id_list:
                ids = id_list.split(',')
                for id in ids:
                    try:
                        id = int(id)
                        _ = self._model.get_vlan('number', id)
                    except Exception:
                        raise exceptions.CommandSyntaxError(command=command)
            else:
                try:
                    id = int(id_list)
                    _ = self._model.get_vlan('number', id)
                except Exception:
                    raise exceptions.CommandSyntaxError(command=command)
            id_list = id_list + '(u)'
            interface.set('allowed_vlan', id_list)

        elif self._validate(args, 'native', 'vlan', str): #untagged
            vlan_id, = self._dissect(args, 'native', 'vlan', str)
            interface = self.get_actual_interface(command)
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            interface.set('native_vlan', int(vlan_id))

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pppoe(self, command, *args, context=None):
        if self._validate(args, 'intermediate-agent', 'port-enable'):
            pass             # No visible changes

        elif self._validate(args, 'intermediate-agent', 'trust'):
            pass             # No visible changes

        elif self._validate(args, 'intermediate-agent', 'port-format-type', 'circuit-id', str):
            pass             # No visible changes

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ip(self, command, *args, context=None):
        if self._validate(args, 'dhcp', 'snooping'):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'trust'):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'information', 'option', 'circuit-id', 'tr101', 'node-identifier',
                            'ip'):
            pass             # No visible changes

        elif self._validate(args, 'dhcp', 'snooping', 'information', 'option', 'circuit-id', 'tr101', 'no-vlan-field'):
            pass             # No visible changes

        else:
            raise exceptions.CommandSyntaxError(command=command)
