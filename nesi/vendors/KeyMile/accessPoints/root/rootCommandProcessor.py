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

class RootCommandProcessor(BaseCommandProcessor):
    __name__ = 'root'
    management_functions = {'main', 'cfgm', 'fm', 'status'}
    access_points = ('eoam', 'fan', 'multicast', 'services', 'tdmConnections')

    from .rootManagementFunctions import main
    from .rootManagementFunctions import cfgm
    from .rootManagementFunctions import fm
    from .rootManagementFunctions import status

    def do_get(self, command, *args, context=None):
        if self._validate(args, "CurrTemperature"):
            context['currTemperature'] = self._model.currTemperature
            context['spacer'] = self.create_spacers((67,), (context['currTemperature'],))[0] * ' '
            self._write(self._render('currTemperature', 'login', 'base', 'get', context=context))

    def _init_access_points(self, context=None):
        self.access_points = ('eoam', 'fan', 'multicast', 'services', 'tdmConnections')
        for card in self._model.cards:
            if 'unit-' + card.name in self.access_points:
                continue
            self.access_points += ('unit-' + card.name,)

        first_unit = 0
        unit_count = 0
        if self._model.version == '2500':
            first_unit = 1
            unit_count = 21
        elif self._model.version == '2300':
            first_unit = 7
            unit_count = 8
        elif self._model.version == '2200':
            first_unit = 9
            unit_count = 4

        for i in range(first_unit, first_unit + unit_count):
            if 'unit-' + str(i) in self.access_points:
                continue

            if 'unit-' + str(i - 1) not in self.access_points:
                self.access_points += (i,)
            else:
                self.access_points = self.access_points[:self.access_points.index('unit-' + str(i - 1)) + 1] + ('unit-' + str(i),) + self.access_points[self.access_points.index('unit-' + str(i - 1)) + 1:]

    def _init_context(self, context=None):
        context['ls_Name'] = self._model.model + ' ' + self._model.version
        context['ls_MainMode'] = ''
        context['ls_EquipmentState'] = 'Ok'

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'VlanId', str) and context['path'].split('/')[-1] == 'cfgm':
            vlan_id, = self._dissect(args, 'VlanId', str)
            vlan_id = int(vlan_id)
            if not 1 < vlan_id < 4089:
                raise exceptions.CommandExecutionError(template='syntax_error',
                                                       template_scopes=('login', 'base', 'syntax_errors'),
                                                       command=None)

            self._model.set_vlan_id(vlan_id)
        elif self._validate(args, 'IP_Address', str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            new_ip, net_mask, gateway = self._dissect(args, 'IP_Address', str, str, str)

            self._model.set_mgmt_address(new_ip)
            self._model.set_net_mask(net_mask)
            self._model.set_default_gateway(gateway)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def do_save(self, command, *args, context=None):
        if len(args) == 0 and context['path'].split('/')[-1] == 'cfgm':
            pass
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_property(self, command, *args, context=None):
        scopes = ('login', 'base', 'get')
        if self._validate(args, "CurrTemperature") and context['path'].split('/')[-1] == 'status':
            context['currTemperature'] = self._model.currTemperature
            context['spacer'] = self.create_spacers((67,), (context['currTemperature'],))[0] * ' '
            self._write(self._render('currTemperature', *scopes, context=context))
        elif self._validate(args, 'IP_Address') and context['path'].split('/')[-1] == 'cfgm':
            context['ip_address'] = self._model.mgmt_address
            context['spacer1'] = self.create_spacers((67,), (self._model.mgmt_address,))[0] * ' '

            context['net_mask'] = self._model.net_mask
            context['spacer2'] = self.create_spacers((67,), (self._model.net_mask,))[0] * ' '

            context['default_gateway'] = self._model.default_gateway
            context['spacer3'] = self.create_spacers((67,), (self._model.default_gateway,))[0] * ' '
            self._write(self._render('ip_address', *scopes, context=context))
        elif self._validate(args, 'VlanId') and context['path'].split('/')[-1] == 'cfgm':
            context['vlan_id'] = self._model.network_element_management_vlan_id
            context['spacer'] = self.create_spacers((67,), (context['vlan_id'],))[0] * ' '
            self._write(self._render('vlan_id', *scopes, context=context))
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))
