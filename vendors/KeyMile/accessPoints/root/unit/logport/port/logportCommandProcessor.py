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
from vendors.KeyMile.accessPoints.root.unit.port.portCommandProcessor import PortCommandProcessor


class LogportCommandProcessor(PortCommandProcessor):
    __name__ = 'logport'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status', 'ifMIB')
    access_points = ()

    from .logportManagementFunctions import main
    from .logportManagementFunctions import cfgm
    from .logportManagementFunctions import fm
    from .logportManagementFunctions import pm
    from .logportManagementFunctions import status
    from .logportManagementFunctions import ifMIB

    def get_property(self, command, *args, context=None):
        port = self.get_port_component()
        scopes = ('login', 'base', 'get')
        try:
            super().get_property(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'AttainableRate') and context['path'].split('/')[-1] == 'status':
                text = self._render('attainable_rate', *scopes, context=context)
                self._write(text)
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def get_port_component(self):
        return self._model.get_logport('name', self._parent._parent.component_id + '/L/' + self.component_id)

    def _init_access_points(self, context=None):
        self.access_points = ()
        logport_name = self._parent._parent.component_id + '/L/' + self.component_id
        logport = self._model.get_logport('name', logport_name)
        try:
            _ = self._model.get_interface('logport_id', logport.id)
        except exceptions.SoftboxenError:
            pass
        else:
            for interface in self._model.get_interfaces('logport_id', logport.id):
                identifier = 'interface-' + interface.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

    def do_deleteinterface(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent._parent.component_id)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and card.product == 'sdsl':
            # all or interface_id
            name, = self._dissect(args, str)
            if name == 'all':
                logport_name = self._parent._parent.component_id + '/L/' + self.component_id
                logport = self._model.get_logport('name', logport_name)
                for interface in self._model.get_interfaces('logport_id', logport.id):
                    interface.delete()
            elif name.startswith('interface-'):
                id = name.split('-')[1]
                try:
                    interface = self._model.get_interface('name', self._parent._parent.component_id + '/L/' + self.component_id + '/' + id)
                    interface.delete()
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_createinterface(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name', self._parent._parent.component_id)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and card.product == 'sdsl':
            # vcc profile and vlan profile
            vlan_prof, = self._dissect(args, str)
            # TODO: Check if profiles := default or profile names
            try:
                logport_name = self._parent._parent.component_id + '/L/' + self.component_id
                logport = self._model.get_logport('name', logport_name)
                id = 1
                for interface in self._model.get_interfaces('logport_id', logport.id):
                    if interface.logport_id is not None:
                        new_id = int(interface.name[-1]) + 1
                        id = new_id if new_id > id else id
                try:
                    name = self._parent._parent.component_id + '/L/' + self.component_id + '/' + str(id)
                    _ = self._model.get_interface('name',  name)
                    assert False
                except exceptions.SoftboxenError as exe:
                    vcc = self._model.add_interface(name=name, logport_id=logport.id, vlan_profile=vlan_prof)
                    context['spacer1'] = self.create_spacers((57,), (str(id),))[0] * ' '
                    context['id'] = str(id)
                    # TODO: Template is unknown
                    text = self._render('interface_success', *scopes, context=context)
                    self._write(text)
                except AssertionError:
                    raise exceptions.CommandSyntaxError(command=command)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        try:
            super().set(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate(args, *()):
                exc = exceptions.CommandSyntaxError(command=command)
                exc.template = 'syntax_error'
                exc.template_scopes = ('login', 'base', 'syntax_errors')
                raise exc
            elif self._validate(args, 'test', str):
                ip, = self._dissect(args, 'test', str)
                # TODO test case
                return
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
