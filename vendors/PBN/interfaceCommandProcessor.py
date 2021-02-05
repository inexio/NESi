# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class InterfaceCommandProcessor(BaseCommandProcessor):

    def get_component(self, command, *args, context=None):
        portname = context['component'].name
        try:
            port = self._model.get_port('name', portname)
        except exceptions.SoftboxenError:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
            ('login', 'mainloop', 'ena', 'conf', 'interface'))

        return port

    def do_exit(self, command, *args, context=None):
        from .confCommandProcessor import ConfCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = ConfCommandProcessor
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        elif self._validate(command, '!'):
            port = self.get_component(command, args, context=context)
            port.set('exclamation_mark', True)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_shutdown(self, command, *args, context=None):
        if len(args) == 0:
            port = self.get_component(command, args, context=context)
            port.admin_up()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_shutdown(self, command, *args, context=None):
        if len(args) == 0:
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_description(self, command, *args, context=None):
        if len(args) > 0:
            descr = ''
            for x in args:
                descr += (x + ' ')
            descr = descr[:-1]
            port = self.get_component(command, args, context=context)
            port.set('description', descr)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_spanning_tree(self, command, *args, context=None):
        if self._validate(args, 'guard', 'root'):
            port = self.get_component(command, args, context=context)
            port.set('spanning_tree_guard_root', True)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_switchport(self, command, *args, context=None):
        if self._validate(args, 'trunk', 'vlan-allowed', str):          # switchport_trunk_vlan_allowed
            vlan, = self._dissect(args, 'trunk', 'vlan-allowed', str)
            try:
                _ = self._model.get_vlan('number', vlan)
            except:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)
            port = self.get_component(command, args, context=context)
            port.set('switchport_trunk_vlan_allowed', vlan + ',')
        elif self._validate(args, 'mode', 'trunk'):         # switchport_mode_trunk
            port = self.get_component(command, args, context=context)
            port.set('switchport_mode_trunk', True)
        elif self._validate(args, 'pvid', str):             # switchport_pvid
            pvid, = self._dissect(args, 'pvid', str)
            pvid = int(pvid)
            port = self.get_component(command, args, context=context)
            port.set('switchport_pvid', pvid)
        elif self._validate(args, 'block', 'multicast'):    # switchport_block_multicast
            port = self.get_component(command, args, context=context)
            port.set('switchport_block_multicast', True)
        elif self._validate(args, 'rate-limit', str, 'egress'):     # switchport_rate_limit_egress
            value, = self._dissect(args,  'rate-limit', str, 'egress')
            value = int(value)
            port = self.get_component(command, args, context=context)
            port.set('switchport_rate_limit_egress', value)
        elif self._validate(args, 'rate-limit', str, 'ingress'):    # switchport_rate_limit_ingress
            value, = self._dissect(args, 'rate-limit', str, 'ingress')
            value = int(value)
            port = self.get_component(command, args, context=context)
            port.set('switchport_rate_limit_ingress', value)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_lldp(self, command, *args, context=None):
        if self._validate(args, 'transmit'):
            port = self.get_component(command, args, context=context)
            port.set('no_lldp_transmit', True)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_speed(self, command, *args, context=None):
        if self._validate(args, str):
            limit, = self._dissect(args, str)
            limit = int(limit)
            port = self.get_component(command, args, context=context)
            port.set('pbn_speed', limit)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)
