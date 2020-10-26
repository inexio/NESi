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


class InterfaceCommandProcessor(BaseCommandProcessor):
    __name__ = 'interface'
    management_functions = ('main', 'cfgm', 'pm', 'status')
    access_points = ()

    from .interfaceManagementFunctions import main
    from .interfaceManagementFunctions import cfgm
    from .interfaceManagementFunctions import pm
    from .interfaceManagementFunctions import status

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'test', str):
            ip, = self._dissect(args, 'test', str)
            #TODO test case
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_component(self):
        return self._model.get_interface('name', self.component_name)

    def get_property(self, command, *args, context=None):
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'ServiceStatus') and context['path'].split('/')[-1] == 'status':
            vcc = self.get_component()
            context['spacer1'] = self.create_spacers((67,), (vcc.vcc_profile,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (vcc.vlan_profile,))[0] * ' '
            text = self._render('service_status', *scopes, context=dict(context, vcc=vcc))
            self._write(text)
        elif self._validate(args, 'configuredProfiles') and context['path'].split('/')[-1] == 'cfgm':
            vcc = self.get_component()
            services_connected = '"' + vcc.services_connected + '"'
            context['vcc_services_connected'] = services_connected
            context['spacer1'] = self.create_spacers((67,), (vcc.number_of_conn_services,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (vcc.reconfiguration_allowed,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (services_connected,))[0] * ' '
            text = self._render('configured_profiles', *scopes, context=dict(context, vcc=vcc))
            self._write(text)
        elif self._validate(args, 'VlanProfile') and context['path'].split('/')[-1] == 'cfgm':
            vcc = self.get_component()
            context['spacer1'] = self.create_spacers((67,), (vcc.vlan_profile,))[0] * ' '
            text = self._render('vlan_profile', *scopes, context=dict(context, vcc=vcc))
            self._write(text)
        elif self._validate(args, 'IfRateLimiting') and context['path'].split('/')[-1] == 'cfgm':
            vcc = self.get_component()
            text = self._render('if_rate_limiting', *scopes, context=dict(context, vcc=vcc))
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)
