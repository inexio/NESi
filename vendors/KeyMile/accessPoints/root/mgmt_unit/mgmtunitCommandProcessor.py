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
import time

from nesi import exceptions
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class MgmtunitCommandProcessor(BaseCommandProcessor):
    __name__ = 'mgmtunit'
    management_functions = ('main', 'fm')
    access_points = ()  # 'internalPorts', only on certain cards

    from .mgmtunitManagementFunctions import main
    from .mgmtunitManagementFunctions import cfgm
    from .mgmtunitManagementFunctions import fm
    from .mgmtunitManagementFunctions import status

    def _init_access_points(self, context=None):
        self.access_points = ()
        try:
            card = self.get_component()

            self.management_functions = ('main', 'cfgm', 'fm', 'status')

            for port in self._model.get_mgmt_ports('mgmt_card_id', card.id):
                identifier = 'port-' + port.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

        except exceptions.InvalidInputError:
            pass

    def get_property(self, command, *args, context=None):
        card = self.get_component()
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'Labels') and context['path'].split('/')[-1] == 'main':
            context['spacer1'] = self.create_spacers((67,), (card.label1,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.label2,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.description,))[0] * ' '
            text = self._render('labels', *scopes, context=dict(context, port=card))
            self._write(text)
        elif self._validate(args, 'EquipmentInventory') and context['path'].split('/')[-1] == 'main':
            unit_symbol = '"' + card.board_name + '"'
            context['unit_symbol'] = unit_symbol
            context['spacer_1'] = self.create_spacers((67,), (unit_symbol,))[0] * ' '
            unit_short_text = '"' + card.short_text + '"'
            context['unit_short_text'] = unit_short_text
            context['spacer_2'] = self.create_spacers((67,), (unit_short_text,))[0] * ' '
            unit_board_id = card.board_id
            context['unit_board_id'] = unit_board_id
            context['spacer_3'] = self.create_spacers((67,), (unit_board_id,))[0] * ' '
            unit_hardware_key = card.hardware_key
            context['unit_hardware_key'] = unit_hardware_key
            context['spacer_4'] = self.create_spacers((67,), (unit_hardware_key,))[0] * ' '
            unit_manufacturer_id = '"' + card.manufacturer_id + '"'
            context['unit_manufacturer_id'] = unit_manufacturer_id
            context['spacer_5'] = self.create_spacers((67,), (unit_manufacturer_id,))[0] * ' '
            unit_serial_number = '"' + card.serial_number + '"'
            context['unit_serial_number'] = unit_serial_number
            context['spacer_6'] = self.create_spacers((67,), (unit_serial_number,))[0] * ' '
            unit_manufacturer_part_number = '"' + card.manufacturer_part_number + '"'
            context['unit_manufacturer_part_number'] = unit_manufacturer_part_number
            context['spacer_7'] = self.create_spacers((67,), (unit_manufacturer_part_number,))[0] * ' '
            unit_manufacturer_build_state = '"' + card.manufacturer_build_state + '"'
            context['unit_manufacturer_build_state'] = unit_manufacturer_build_state
            context['spacer_8'] = self.create_spacers((67,), (unit_manufacturer_build_state,))[0] * ' '
            unit_supplier_part_number = '"' + card.model_name + '"'
            context['unit_supplier_part_number'] = unit_supplier_part_number
            context['spacer_9'] = self.create_spacers((67,), (unit_supplier_part_number,))[0] * ' '
            unit_supplier_build_state = '"' + card.supplier_build_state + '"'
            context['unit_supplier_build_state'] = unit_supplier_build_state
            context['spacer_10'] = self.create_spacers((67,), (unit_supplier_build_state,))[0] * ' '
            unit_customer_id = '"' + card.customer_id + '"'
            context['unit_customer_id'] = unit_customer_id
            context['spacer_11'] = self.create_spacers((67,), (unit_customer_id,))[0] * ' '
            unit_customer_product_id = '"' + card.customer_product_id + '"'
            context['unit_customer_product_id'] = unit_customer_product_id
            context['spacer_12'] = self.create_spacers((67,), (unit_customer_product_id,))[0] * ' '
            unit_boot_loader = '"' + card.boot_loader + '"'
            context['unit_boot_loader'] = unit_boot_loader
            context['spacer_13'] = self.create_spacers((67,), (unit_boot_loader,))[0] * ' '
            unit_processor = '"' + card.processor + '"'
            context['unit_processor'] = unit_processor
            context['spacer_14'] = self.create_spacers((67,), (unit_processor,))[0] * ' '
            text = self._render('equipment_inventory', *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def get_component(self):
        return self._model.get_mgmt_card('name', self.component_name)

    def set(self, command, *args, context=None):
        try:
            card = self.get_component()
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'Labels', str, str, str) and context['path'].split('/')[-1] == 'main':
            label1, label2, description = self._dissect(args, 'Labels', str, str, str)
            try:
                component = self.get_component()
                component.set_label(label1, label2, description)
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        else:
            raise exceptions.CommandSyntaxError(command=command)

