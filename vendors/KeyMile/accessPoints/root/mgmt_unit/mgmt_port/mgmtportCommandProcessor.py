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
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor
import time


class MgmtportCommandProcessor(BaseCommandProcessor):
    __name__ = 'mgmtport'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .mgmtportManagementFunctions import main
    from .mgmtportManagementFunctions import cfgm
    from .mgmtportManagementFunctions import fm
    from .mgmtportManagementFunctions import pm
    from .mgmtportManagementFunctions import status

    def get_property(self, command, *args, context=None):
        port = self.get_component()
        card = self._model.get_card('name', self.component_name.split('/')[0])
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc

        elif self._validate((args[0],), 'AdministrativeStatus') and context['path'].split('/')[-1] == 'main':
            self.map_states(port, 'port')
            context['spacer'] = self.create_spacers((67,), (port.admin_state,))[0] * ' '
            text = self._render('administrative_status', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'Labels') and context['path'].split('/')[-1] == 'main':
            context['spacer1'] = self.create_spacers((67,), (port.label1,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (port.label2,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (port.description,))[0] * ' '
            text = self._render('labels', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate((args[0],), 'OperationalStatus') and context['path'].split('/')[-1] == 'main':
            self.map_states(port, 'port')
            port_operational_state = port.operational_state
            context['port_operational_state'] = port_operational_state
            context['spacer'] = self.create_spacers((67,), (port_operational_state,))[0] * ' '
            text = self._render('operational_status', *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        self.access_points = ()
        return

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def get_component(self):
        return self._model.get_mgmt_port('name', self.component_name)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name', self.component_name.split('/')[0])
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'AdministrativeStatus', str) and context['path'].split('/')[-1] == 'main':
            state, = self._dissect(args, 'AdministrativeStatus', str)
            try:
                port = self.get_component()
                if state == 'up':
                    port.admin_up()
                elif state == 'down':
                    port.admin_down()
                else:
                    raise exceptions.SoftboxenError()
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'Labels', str, str, str) and context['path'].split('/')[-1] == 'main':
            label1, label2, description = self._dissect(args, 'Labels', str, str, str)
            try:
                port = self.get_component()
                port.set_label(label1, label2, description)
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        else:
            raise exceptions.CommandSyntaxError(command=command)
