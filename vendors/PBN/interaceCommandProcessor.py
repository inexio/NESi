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
            print('!')      # TODO: find functionality
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

    def do_description(self, command, *args, context=None): #TODO
        if self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_spanning_tree(self, command, *args, context=None): #TODO
        if self._validate(args, 'guard', 'root'):
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_switchport(self, command, *args, context=None): #TODO
        if self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        elif self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        elif self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        elif self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        elif self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        elif self._validate(args, str):
            descr, = self._dissect(args, str)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_lldp(self, command, *args, context=None): #TODO
        if self._validate(args, 'transmit'):
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_speed(self, command, *args, context=None): #TODO
        if self._validate(args, str):
            limit, = self._dissect(args, str)
            limit = int(limit)
            port = self.get_component(command, args, context=context)
            port.admin_down()
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)
