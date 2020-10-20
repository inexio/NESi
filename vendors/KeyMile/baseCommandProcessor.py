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

    component_id = None

    def set_component_id(self, id):
        self.component_id = id

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
                object.admin_state = 'Up'
        elif object.admin_state == '2':
            if type == 'port':
                object.admin_state = 'Locked'
        elif object.admin_state == '3':
            if type == 'port':
                object.admin_state = 'Unlocked'

        if object.operational_state == '0':
            if type == 'port':
                object.operational_state = 'Down'
        elif object.operational_state == '1':
            if type == 'port':
                object.operational_state = 'Up'

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
        elif self._validate(args, ):
            self._write(self._render('help', *help_scopes, context=context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pwd(self, command, *args, context=None):
        context['spacer'] = self.create_spacers((67,), (context['path'],))[0] * ' '
        self._write(self._render('pwd', 'login', 'base', context=context))

    def ls(self, context=None):
        scopes = ('login', 'base', 'ls')
        if re.search('(pm|fm|status|main|cfgm)', context['path']):
            mf_type = context['path'].split('/')[-1]

            mf_layers = {}
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

            self._init_access_points(context=context)

            text += self._render('ls_mf_list', *scopes, context=context)
            for management_function in self.management_functions:
                context['list_entry'] = management_function
                text += self._render('ls_list_body', *scopes, context=context)

            text += self._render('ls_ap_list', *scopes, context=context)

            for access_point in self.access_points:
                context['list_entry'] = access_point
                text += self._render('ls_list_body', *scopes, context=context)

            self._write(text)

    def do_ls(self, command, *args, context=None):
        if self._validate(args, ):
            self.ls(context=context)
        elif self._validate(args, '-e'):
            pass
        elif self._validate(args, str):
            path = args[0]
            current_path = context['path']

            try:
                tmp_cmdproc = self.change_directory(path, context=context)
                tmp_cmdproc.ls(context=context)
            except exceptions.CommandExecutionError:
                context['path'] = current_path
                raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                       template_scopes=('login', 'base', 'execution_errors'),
                                                       command=None)

            context['path'] = current_path
        else:
            raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                   template_scopes=('login', 'base', 'execution_errors'),
                                                   command=command)

    def change_directory(self, path, context=None):
        path = path.lower()
        if re.search('^(?:[^.]+/)+\.\.$', path):
            raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                   template_scopes=('login', 'base', 'execution_errors'),
                                                   command=None)
        if re.search('^(?:[^.]+/)+\.\.(?:/.+)+$', path):
            raise exceptions.CommandExecutionError(template='invalid_address_error',
                                                   template_scopes=('login', 'base', 'execution_errors'),
                                                   command=None)

        if path == '/':
            if self.__name__ != 'root':
                return self._parent.change_directory(path, context=context)
            else:
                context['path'] = '/'
                return self

        components = [x for x in path.split('/') if x]

        if not re.search(
                '^(unit-[0-9]+|port-[0-9]+|portgroup-[0-9]+|chan-[0-9]+|interface-[0-9]+|vcc-[0-9]+|alarm-[0-9]+|main|cfgm|fm|pm|status|eoam|fan|multicast|services|packet|subpacket|srvc-[0-9]|macaccessctrl|tdmconnections|logports|logport-[0-9]|1to1doubletag|1to1singletag|mcast|nto1|pls|tls|\.|\.\.)$',
                components[0]):
            raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                       template_scopes=('login', 'base', 'execution_errors'),
                                                       command=None)

        if path == '.':
            return self

        if path.startswith('./'):
            if path == './':
                return self

            return self.change_directory(path[2:], context=context)

        if path.startswith('..'):
            splitted_path = [x for x in context['path'].split('/') if x]
            exit_component = None
            if len(splitted_path) != 0:
                exit_component = splitted_path.pop()
            context['path'] = '/' + '/'.join(splitted_path)

            if exit_component in ('main', 'cfgm', 'fm', 'pm', 'status'):
                self.set_prompt_end_pos(context=context)
                if path != '..':
                    return self.change_directory(path[3:], context=context)
                return self

            if path == '..':
                if self.__name__ == 'root':
                    return self
                return self._parent

            if self.__name__ == 'root':
                return self.change_directory(path[3:], context=context)

            return self._parent.change_directory(path[3:], context=context)
        if path.startswith('/'):
            if 'unit-' not in components[0] and components[0] not in (
                    'eoam', 'fan', 'multicast', 'services', 'tdmConnection', 'main', 'cfgm', 'fm', 'pm', 'status'):
                raise exceptions.CommandExecutionError(command=None, template=None,
                                                       template_scopes=())  # TODO: fix exception to not require all fields as empty

            if self.__name__ != 'root':
                subprocessor = self._parent.change_directory(path, context=context)
            else:
                context['path'] = '/'
                subprocessor = self.change_directory(path.lstrip('/'), context=context)
        else:
            remaining_args = '/'.join(components[1:])

            component_type = None
            component_id = None
            if '-' in components[0]:
                component_type = components[0].split('-')[0]
                component_id = components[0].split('-')[1]
                if component_type == 'port':
                    if self.__name__ == 'portgroup':
                        component_type = 'portgroupport'
                    elif self.__name__ == 'mgmtunit':
                        component_type = 'mgmtport'
                if component_type == 'unit':
                    if component_id == '11' or component_id == '13':
                        component_type = 'mgmtunit'

                command_processor = component_type.capitalize() + 'CommandProcessor'
            else:
                if components[0] in ('1to1doubletag', '1to1singletag', 'mcast', 'nto1', 'pls', 'tls'):
                    if context['path'].split('/')[-1] in (
                    '1to1doubletag', '1to1singletag', 'mcast', 'nto1', 'pls', 'tls'):
                        raise exceptions.CommandExecutionError(command=None, template=None,
                                                               template_scopes=())  # TODO: fix exception to not require all fields as empty

                    context['ServiceType'] = components[0]

                    command_processor = 'SubpacketCommandProcessor'
                else:
                    command_processor = components[0].capitalize() + 'CommandProcessor'

            if component_type == 'unit':
                if (self._model.version == '2200' and not 9 <= int(component_id) <= 12) or (self._model.version == '2300' and not 7 <= int(component_id) <= 14) or (self._model.version == '2500' and not 1 <= int(component_id) <= 21):
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty#
                if self.__name__ != 'root':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'portgroup' or component_type == 'logports' or component_type == 'huntgroup':
                if self.__name__ != 'unit':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'port':
                try:
                    if self.component_id == '11' or self.component_id == '13':
                        self._model.get_mgmt_port('name', self.component_id + '/' + component_id)
                    else:
                        self._model.get_port('name', self.component_id + '/' + component_id)
                except exceptions.InvalidInputError:
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty

                if self.__name__ != 'unit' and self.__name__ != 'portgroup':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'chan':
                if self.__name__ != 'port':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'mgmtunit':
                if self.__name__ != 'root':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'mgmtport':
                if self.__name__ != 'mgmtunit':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'interface':
                if self.__name__ != 'port' and self.__name__ != 'chan' and self.__name__ != 'logport':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'logport':
                if self.__name__ != 'logports':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            elif component_type == 'vcc':
                if self.__name__ != 'chan':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty

            elif components[0] in ('packet', 'macAccessCtrl'):
                if self.__name__ != 'services':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            if components[0] in ('fan', 'eoam', 'tdmConnections', 'multicast', 'services'):
                if self.__name__ != 'root':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty
            if components[0] in ('1to1doubletag', '1to1singletag', 'mcast', 'nto1', 'pls', 'tls'):
                if self.__name__ != 'packet':
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                           template_scopes=())  # TODO: fix exception to not require all fields as empty

            if components[0] in ('main', 'cfgm', 'fm', 'pm', 'status'):
                if context['path'].split('/')[-1] in ('main', 'cfgm', 'fm', 'pm', 'status'):
                    raise exceptions.CommandExecutionError(command=None, template='invalid_address_error', template_scopes=('login', 'base', 'execution_errors'))

                mf_layers = {}
                if components[0] == 'status':
                    mf_layers = self.status
                elif components[0] == 'cfgm':
                    mf_layers = self.cfgm
                elif components[0] == 'fm':
                    mf_layers = self.fm
                elif components[0] == 'pm':
                    mf_layers = self.pm
                elif components[0] == 'main':
                    mf_layers = self.main

                if len(mf_layers) == 0:
                    raise exceptions.CommandExecutionError(command=None, template=None,
                                                     template_scopes=())  # TODO: fix exception to not require all fields as empty

                if context['path'] == '/':
                    new_path = components[0]
                else:
                    new_path = '/' + components[0]
                context['path'] += new_path
                return self

            from vendors.KeyMile.accessPoints.root.unit.unitCommandProcessor import UnitCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.portCommandProcessor import PortCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.chan.chanCommandProcessor import ChanCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.interface.interfaceCommandProcessor import \
                InterfaceCommandProcessor
            from vendors.KeyMile.accessPoints.root.fan.fanCommandProcessor import FanCommandProcessor
            from vendors.KeyMile.accessPoints.root.fan.alarmCommandProcessor import AlarmCommandProcessor
            from vendors.KeyMile.accessPoints.root.eoamCommandProcessor import EoamCommandProcessor
            from vendors.KeyMile.accessPoints.root.multicastCommandProcessor import MulticastCommandProcessor
            from vendors.KeyMile.accessPoints.root.tdmconnectionsCommandProcessor import TdmconnectionsCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.servicesCommandProcessor import ServicesCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.portgroup.portgroupCommandProcessor import \
                PortgroupCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.portgroup.port.portgroupportCommandProcessor import \
                PortgroupportCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.logport.logportsCommandProcessor import LogportsCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.logport.port.logportCommandProcessor import \
                LogportCommandProcessor
            from vendors.KeyMile.accessPoints.root.unit.port.chan.vcc.vccCommandProcessor import VccCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.packetCommandProcessor import PacketCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.macaccessctrlCommandProcessor import \
                MacaccessctrlCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.subpacketCommandProcessor import SubpacketCommandProcessor
            from vendors.KeyMile.accessPoints.root.services.srvcCommandProcessor import SrvcCommandProcessor
            from vendors.KeyMile.accessPoints.root.mgmt_unit.mgmtunitCommandProcessor import MgmtunitCommandProcessor
            from vendors.KeyMile.accessPoints.root.mgmt_unit.mgmt_port.mgmtportCommandProcessor import MgmtportCommandProcessor
            subprocessor = self._create_subprocessor(eval(command_processor), 'login', 'base')

            if component_id is not None and self.component_id is not None:
                subprocessor.set_component_id(self.component_id + '/' + component_id)

            if component_id is not None:
                subprocessor.set_component_id(component_id)

            if context['path'] == '/':
                new_path = components[0]
            else:
                if path == 'subpacket':
                    new_path = '/' + context['ServiceType']
                else:
                    new_path = '/' + components[0]
            context['path'] += new_path

            if len(remaining_args) > 0:
                subprocessor = subprocessor.change_directory(remaining_args, context=context)

        return subprocessor

    def do_get(self, command, *args, context=None):
        if len(args) >= 1:
            if '/' in args[0]:
                path = ''
                for component in args[0].split('/')[:-1]:
                    path += component + '/'
                prop = args[0].split('/')[-1]
                try:
                    tmp_cmdproc = self.change_directory(path, context=context)
                    tmp_cmdproc.get_property(command, *prop, context=context)
                except exceptions.CommandExecutionError:
                    raise exceptions.CommandExecutionError(template='syntax_error',
                                                           template_scopes=('login', 'base', 'syntax_errors'),
                                                           command=None)
            else:
                self.get_property(command, args[0], context=context)
        else:
            raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                   template_scopes=('login', 'base', 'execution_errors'),
                                                   command=None)

    def get_property(self, command, *args, context=None):
        raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                               template_scopes=('login', 'base', 'execution_errors'))

    def do_set(self, command, *args, context=None):
        if len(args) == 0:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))
        elif args[0].count('/') > 0:
            path = ''
            for el in args[0].split('/')[:-1]:
                path += el + '/'
            proc = self.change_directory(str(path[:-1]), context=context)
            res = (args[0].split('/')[-1],) + args[1:]
            proc.set(command, *res, context=context)
        elif args[0].count('/') == 0:
            self.set(command, *args, context=context)

        return

    def set(self, command, *args, context=None):
        # interface method
        return

    def do_cd(self, command, *args, context=None):
        if self._validate(args, ):
            raise exceptions.CommandSyntaxError()
        elif self._validate(args, str):
            path = args[0]
            current_path = context['path']
            try:
                subprocessor = self.change_directory(path, context=context)
            except:
                context['path'] = current_path
                raise
            subprocessor.loop(context=context, return_to=subprocessor._parent)
        else:
            raise exceptions.CommandExecutionError(template='invalid_management_function_error',
                                                   template_scopes=('login', 'base', 'execution_errors'),
                                                   command=command)

    def do_exit(self, command, *args, context=None):
        exc = exceptions.TerminalExitError()
        exc.return_to = 'sysexit'
        raise exc

    def _init_access_points(self, context=None):
        pass  # Abstract method not implemented
