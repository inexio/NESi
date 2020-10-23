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
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class SrvcCommandProcessor(BaseCommandProcessor):
    __name__ = 'srvc'
    management_functions = ('main', 'cfgm', 'status')
    access_points = ()

    from .srvcManagementFunctions import main
    from .srvcManagementFunctions import cfgm
    from .srvcManagementFunctions import status

    def get_property(self, command, *args, context=None):
        service_name = self.component_name
        services = self._model.get_srvcs('name', service_name)
        service = None
        for s in services:
            if s.service_type.lower() == context['ServiceType'] and s.name == service_name:
                service = s
                context['service'] = service
                break

        if not service:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

        scopes = ('login', 'base', 'get')
        if self._validate((args[0],), 'Service') and context['path'].split('/')[-1] == 'cfgm':
            # TODO: Find missing templates, and replace placeholder templates
            if service.service_type == '1to1doubletag':
                template_name = 'service_onetoonedoubletag'
            elif service.service_type == '1to1singletag':
                template_name = 'service_onetoonesingletag'
            elif service.service_type == 'mcast':
                template_name = 'service_mcast'
            elif service.service_type == 'nto1':
                template_name = 'service_nto1'
            elif service.service_type == 'pls':
                template_name = 'service_pls'
            elif service.service_type == 'tls':
                template_name = 'service_tls'
            else:
                raise exceptions.CommandExecutionError(command=command)
            context['spacer1'] = self.create_spacers((67,), (service.address,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (service.svid,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (service.stag_priority,))[0] * ' '
            context['spacer4'] = self.create_spacers((67,), (service.vlan_handling,))[0] * ' '
            text = self._render(template_name, *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'Service', str, str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            address, svid, stag, vlan = self._dissect(args, 'Service', str, str, str, str)
            try:
                service_name = self.component_name
                services = self._model.get_srvcs('name', service_name)
                service = None
                for s in services:
                    if s.service_type.lower() == context['ServiceType'] and s.name == service_name:
                        service = s
                        break

                if not service:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))

                service.set_service(address, int(svid), stag, vlan)
            except exceptions.SoftboxenError:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def get_component(self):
        return self._model.get_srvcs('name', self.component_name)
