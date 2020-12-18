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


class PortgroupCommandProcessor(BaseCommandProcessor):
    __name__ = 'portgroup'
    management_functions = ('main', 'cfgm')
    access_points = ()

    from .portgroupManagementFunctions import main
    from .portgroupManagementFunctions import cfgm

    def _init_access_points(self, context=None):    # work in progress
        self.access_points = ()
        card = self._model.get_card('name', self.component_name.split('/')[0])

        for gport in self._model.get_portgroupports('card_id', card.id):
            if gport.name.split('/')[1] == 'G' + self.component_name.split('/')[-1][1:]:
                identifier = 'port-' + gport.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

    def _init_context(self, context=None):
        context['ls_Name'] = 'ISDN-BA'
        context['ls_MainMode'] = '16 Ports'
        context['ls_EquipmentState'] = ''

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        else:
            raise exceptions.CommandSyntaxError(command=command)
