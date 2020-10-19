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
        service_name = 'srvc-' + self.component_id
        services = self._model.get_srvcs('name', service_name)
        for s in services:
            if s.service_type == context['ServiceType']:
                service = s
                context['service'] = service
                break
        scopes = ('login', 'base', 'get')
        try:
            super().get_property(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'Service') and context['component_path'].split('/')[-1] == 'cfgm':
                if service.service_type == '1to1DoubleTag':
                    template_name = 'service_onetoonedoubletag'
                elif service.service_type == '1to1SingleTag':
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
                text = self._render(template_name, *scopes, context=context)
                self._write(text)

            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
