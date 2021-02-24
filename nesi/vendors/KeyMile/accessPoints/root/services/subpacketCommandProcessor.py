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
from nesi.vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class SubpacketCommandProcessor(BaseCommandProcessor):
    __name__ = 'subpacket'
    management_functions = ('main', 'cfgm')
    access_points = ()

    from .subpacketManagementFunctions import main
    from .subpacketManagementFunctions import cfgm

    def _init_access_points(self, context=None):
        self.access_points = ()
        try:
            self.management_functions = ('main', 'cfgm')
            s_type = context['ServiceType']

            srvcs = self._model.get_srvcs('service_type', s_type)
            for srvc in srvcs:
                identifier = srvc.name
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)
        except exceptions.InvalidInputError:
            pass

    def do_deleteservice(self, command, *args, context=None):
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm':
            srvc_id, = self._dissect(args, str)
            service_name = 'srvc-' + srvc_id
            service = None
            services = self._model.get_srvcs('name', service_name)
            for s in services:
                if s.service_type == context['ServiceType']:
                    service = s
                    break
            if service is None:
                raise exceptions.CommandExecutionError(command=command, template='unknown_service_fragment',
                                                       template_scopes=('login', 'base', 'execution_errors'))
            service.delete()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_createservice(self, command, *args, context=None):
        if context['ServiceType'] == 'nto1' and context['path'].split('/')[-1] == 'cfgm':
            if len(args) == 12:
                address, svid = self._dissect(args[:2], str, str)
                # TODO: validate address
                srvc = self._model.add_srvc(service_type='nto1', address=address, svid=svid)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif context['ServiceType'] == '1to1singletag' and context['path'].split('/')[-1] == 'cfgm':
            if len(args) == 4:
                address, svid = self._dissect(args[:2], str, str)
                # TODO: validate address
                srvc = self._model.add_srvc(service_type='1to1singletag', address=address, svid=svid)

            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)
