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
import re


class BaseCommandProcessor(base.CommandProcessor):
    """Create CLI REPR loop for example switch."""

    management_functions = ()
    access_points = ()

    main = {}

    cfgm = {}

    fm = {}

    pm = {}

    status = {}

    def map_states(self, object, type):
        if object.admin_state == '0':
            if type == 'port':
                object.admin_state = 'Down'
        elif object.admin_state == '1':
            if type == 'port':
                object.admin_state = 'Down'

        if object.operational_state == '0':
            if type == 'port':
                object.operational_state = 'Down'
        elif object.operational_state == '1':
            if type == 'port':
                object.operational_state = 'Down'

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

    def do_help(self, command, *args, context=None):
        help_scopes = ('login', 'base', 'help')
        if self._validate(args, str):
            help_arg, = self._dissect(args, str)

            if help_arg == 'cd':
                self._write(self._render('help_cd', *help_scopes, context=context))
            elif help_arg == 'pwd':
                self._write(self._render('help_pwd', *help_scopes, context=context))
            elif help_arg == 'ls':
                self._write(self._render('help_ls', *help_scopes, context=context))
            elif help_arg == 'show':
                self._write(self._render('help_show', *help_scopes, context=context))
            elif help_arg == 'mode':
                self._write(self._render('help_mode', *help_scopes, context=context))
            elif help_arg == 'ftpserver':
                self._write(self._render('help_ftpserver', *help_scopes, context=context))
            elif help_arg == 'upload':
                self._write(self._render('help_upload', *help_scopes, context=context))
            elif help_arg == 'download':
                self._write(self._render('help_download', *help_scopes, context=context))
            elif help_arg == 'get':
                self._write(self._render('help_get', *help_scopes, context=context))
            elif help_arg == 'set':
                self._write(self._render('help_set', *help_scopes, context=context))
            elif help_arg == 'profile':
                self._write(self._render('help_profile', *help_scopes, context=context))
            elif help_arg == 'help':
                self._write(self._render('help_help', *help_scopes, context=context))
            elif help_arg == 'exit':
                self._write(self._render('help_exit', *help_scopes, context=context))
            else:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args,):
            self._write(self._render('help', *help_scopes, context=context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pwd(self, command, *args, context=None):
        context['spacer'] = self.create_spacers((67,), (context['path'],))[0] * ' '
        self._write(self._render('pwd', 'login', 'base', context=context))

    def exec_in_path(self, path, command, *args, context=None):
        pass

    def do_cd(self, command, *args, context=None):
        if len(args) == 0:
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc

        if args[0] == '/':
            context['path'] = '/'
            from vendors.KeyMile.accessPoints.root.rootCommandProcessor import RootCommandProcessor
            exc = exceptions.TerminalExitError()
            exc.return_to = RootCommandProcessor

            raise exc

        components = [x for x in args[0].split('/') if x]

        if not re.search(
                '^(unit-[0-9]+|port-[0-9]+|chan-[0-9]+|interface-[0-9]+|vcc-[0-9]+|alarm-[0-9]+|main|cfgm|fm|pm|status|eoam|fan|multicast|services|tdmConnection|packet|macAccessCtrl|\.|\.\.)$',
                components[0]):
            raise exceptions.CommandExecutionError(command=None, template=None,
                                                   template_scopes=())  # TODO: fix exception to not require all fields as empty

        if args[0] == '.':
            return  # dot does nothing

        if args[0].startswith('./'):
            if args[0] == './':
                return

            self.do_cd(command, args[0][2:], context=context)
            return

        if re.search('\.\./(?:[^.]+/)+\.\.', args[0]):
            if args[0].endswith('..'):
                raise exceptions.CommandExecutionError(template='invalid_management_function_error', template_scopes=('login', 'base', 'execution_errors'), command=None)
            else:
                raise exceptions.CommandExecutionError(template='invalid_address_error', template_scopes=('login', 'base', 'execution_errors'), command=None)

        if args[0].startswith('..'):
            splitted_path = [x for x in context['path'].split('/') if x]
            exit_component = None
            if len(splitted_path) != 0:
                exit_component = splitted_path.pop()
            context['path'] = '/' + '/'.join(splitted_path)

            if exit_component in ('main', 'cfgm', 'fm', 'pm', 'status'):
                self.set_prompt_end_pos(context=context)
                if args[0] != '..':
                    self.do_cd('cd', args[0][3:], context=context)
                return

            if args[0] == '..':
                raise exceptions.TerminalExitError()

            exc = exceptions.TerminalExitError()
            exc.command = 'cd ' + args[0][3:]
            raise exc

        if args[0].startswith('/'):
            if 'unit-' not in components[0] and components[0] not in ('eoam', 'fan', 'multicast', 'services', 'tdmConnection', 'main', 'cfgm', 'fm', 'pm', 'status'):
                raise exceptions.CommandExecutionError(command=None, template=None, template_scopes=())  # TODO: fix exception to not require all fields as empty

            context['path'] = '/'

            if self.__name__ != 'root':
                exc = exceptions.TerminalExitError()
                from vendors.KeyMile.accessPoints.root.rootCommandProcessor import RootCommandProcessor
                exc.return_to = RootCommandProcessor
                exc.command = 'cd ' + args[0].lstrip('/')
                raise exc

            self.do_cd('cd', args[0].lstrip('/'), context=context)
        else:
            remaining_args = '/'.join(components[1:])

            component_type = None
            component_number = None
            if '-' in components[0]:
                component_type = components[0].split('-')[0]
                component_number = components[0].split('-')[1]
                command_processor = component_type.capitalize() + 'CommandProcessor'
            else:
                command_processor = components[0].capitalize() + 'CommandProcessor'

            if component_type == 'unit':
                if self.__name__ != 'root':
                    raise exceptions.CommandExecutionError(command=None, template=None, template_scopes=())  # TODO: fix exception to not require all fields as empty

                context['unit'] = component_number
            elif component_type == 'port':
                if self.__name__ != 'unit':
                    raise exceptions.CommandExecutionError(command=None, template=None, template_scopes=())  # TODO: fix exception to not require all fields as empty

                context['port'] = component_number
            elif component_type == 'chan':
                if self.__name__ != 'port':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
                context['chan'] = component_number
            elif component_type == 'interface':
                if self.__name__ != 'port' and self.__name__ != 'chan':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
                context['chan'] = component_number

            if components[0] in ('fan', 'eoam', 'tdmConnections', 'multicast', 'services'):
                if self.__name__ != 'root':
                    raise exceptions.CommandExecutionError(command=None, template=None, template_scopes=())  # TODO: fix exception to not require all fields as empty

            if components[0] in ('main', 'cfgm', 'fm', 'pm', 'status'):
                if re.search('(main|cfgm|fm|pm|status)', context['path']):
                    return
                if context['path'] == '/':
                    new_path = components[0]
                else:
                    new_path = '/' + components[0]
                context['path'] += new_path
                self.set_prompt_end_pos(context=context)
                return

            from vendors.KeyMile.accessPoints.root.unit.unitCommandProcessor import UnitCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.portCommandProcessor import PortCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.chan.chanCommandProcessor import ChanCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.interface.interfaceCommandProcessor import InterfaceCommandProcessor
            from vendors.KeyMile.accessPoints.root.fan.fanCommandProcessor import FanCommandProcessor
            from vendors.KeyMile.accessPoints.root.fan.alarmCommandProcessor import AlarmCommandProcessor
            from vendors.KeyMile.accessPoints.root.eoamCommandProcessor import EoamCommandProcessor
            from vendors.KeyMile.accessPoints.root.multicastCommandProcessor import MulticastCommandProcessor
            from vendors.KeyMile.accessPoints.root.tdmConnectionsCommandProcessor import TdmConnectionsCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.servicesCommandProcessor import ServicesCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.packetCommandProcessor import PacketCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.macAccessCtrlCommandProcessor import MacAccessCtrlCommandProcessor as MacaccessctrlCommandProcessor
            subprocessor = self._create_subprocessor(eval(command_processor), 'login', 'base')

            if len(remaining_args) > 0:
                command = 'cd ' + remaining_args
            else:
                command = None

            if context['path'] == '/':
                new_path = components[0]
            else:
                new_path = '/' + components[0]

            context['path'] += new_path
            subprocessor.loop(context=context, return_to=self.__class__, command=command)

    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def do_ls(self, command, *args, context=None):
        if self._validate(args,):
            scopes = ('login', 'base', 'ls')
            if re.search('(pm|fm|status|main|cfgm)', context['path']):
                mf_type = context['path'].split('/')[-1]

                mf_layers = None
                if mf_type == 'status':
                    mf_layers = self.status
                elif mf_type == 'cfgm':
                    mf_layers = self.cfgm
                elif mf_type == 'fm':
                    mf_layers = self.fm
                elif mf_type == 'pm':
                    mf_layers = self.pm
                elif mf_type == 'main':
                    mf_layers = self.main

                def generate_ls_text(layers, depth):
                    text = ''
                    for layer in layers:
                        if layer not in ('Cmd', 'Prop', 'File'):
                            context['mf_layer'] = depth * '  ' + layer
                            text += self._render('ls_mf_header', *scopes, context=context)
                            depth += 1
                            text += generate_ls_text(layers[layer], depth)
                            depth -= 1
                        else:
                            if layer == 'Cmd':
                                prop_type = layer + ' '
                            else:
                                prop_type = layer

                            context['prop_type'] = depth * '  ' + prop_type

                            for property in layers[layer]:
                                context['prop_name'] = property

                                if prop_type in ('File', 'Prop'):
                                    context['prop_rw_rights'] = layers[layer].get(property, '')
                                else:
                                    context['prop_rw_rights'] = ''
                                text += self._render('ls_mf_body', *scopes, context=context)
                    return text

                text = generate_ls_text(mf_layers, 0)
                self._write(text)

            else:
                text = self._render('ls_header', *scopes, context=context)

                text += self._render('ls_mf_list', *scopes, context=context)
                for management_function in self.management_functions:
                    context['list_entry'] = management_function
                    text += self._render('ls_list_body', *scopes, context=context)

                text += self._render('ls_ap_list', *scopes, context=context)

                self._init_access_points(context=context)

                for access_point in self.access_points:
                    context['list_entry'] = access_point
                    text += self._render('ls_list_body', *scopes, context=context)

                self._write(text)
        elif self._validate(args, '-e'):
            pass
        elif self._validate([args[0]], str):
            path = args[0]

            self.do_cd('cd', path, context=context)
        else:
            raise exceptions.CommandExecutionError(template='invalid_management_function_error', template_scopes=('login', 'base', 'execution_errors'), command=command)

    def _init_access_points(self, context=None):
        pass # Abstract method not implemented
