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


class UnitCommandProcessor(BaseCommandProcessor):
    __name__ = 'unit'
    management_functions = ('main', 'cfgm', 'fm', 'status')
    access_points = ()  # 'internalPorts', only on certain cards

    from .unitManagementFunctions import main
    from .unitManagementFunctions import cfgm
    from .unitManagementFunctions import fm
    from .unitManagementFunctions import status

    def _init_access_points(self, context=None):
        card = self._model.get_card('name', context['unit'])

        # if card.type == ?:
        #   self.access_points += ('internalPorts',)
        #

        for port in self._model.get_ports('card_id', card.id):
            identifier = 'port-' + port.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

        # todo: add portgroup to access_points

    def do_get(self, command, *args, context=None):
        card = self._model.get_card('name', context['unit'])
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc

        elif self._validate((args[0],), 'SubscriberList') and context['path'].split('/')[-1] == 'status' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name',
                                                                                                         context[
                                                                                                             'unit']).product == 'analog'):
            text = self._render('subscriberList_top', *scopes, context=context)
            i = 0
            for subscriber in self._model.subscribers:
                if subscriber.type == 'unit':
                    context['i'] = i
                    context['spacer1'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                    context['spacer2'] = self.create_spacers((63,), (subscriber.registration_state,))[0] * ' '
                    context['spacer3'] = self.create_spacers((63,), (subscriber.address,))[0] * ' '

                    i += 1
                    text += self._render('subscriberList_item', *scopes, context=dict(context, subscriber=subscriber))
            text += self._render('subscriberList_bottom', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'SIP') and context['path'].split('/')[-1] == 'cfgm' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name',
                                                                                                         context[
                                                                                                             'unit']).product == 'analog'):
            # TODO: dynamic fields
            text = self._render('sip', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'IP') and context['path'].split('/')[-1] == 'cfgm' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name',
                                                                                                         context[
                                                                                                             'unit']).product == 'analog'):
            # TODO: dynamic fields
            text = self._render('ip', *scopes, context=context)
            self._write(text)

        elif self._validate((args[0],), 'HardwareAndSoftware') and context['path'].split('/')[-1] == 'main':
            unit_hardware = '"' + card.board_name + '"'
            context['unit_hardware'] = unit_hardware
            context['spacer_1'] = self.create_spacers((67,), (unit_hardware,))[0] * ' '
            unit_supplier_build_state = '"' + card.supplier_build_state + '"'
            context['unit_supplier_build_state'] = unit_supplier_build_state
            context['spacer_2'] = self.create_spacers((67,), (unit_supplier_build_state,))[0] * ' '
            unit_board_id = card.board_id
            context['unit_board_id'] = unit_board_id
            context['spacer_3'] = self.create_spacers((67,), (unit_board_id,))[0] * ' '
            unit_hardware_key = card.hardware_key
            context['unit_hardware_key'] = unit_hardware_key
            context['spacer_4'] = self.create_spacers((67,), (unit_hardware_key,))[0] * ' '
            unit_software = '"' + card.software + '"'
            context['unit_software'] = unit_software
            context['spacer_5'] = self.create_spacers((67,), (unit_software,))[0] * ' '
            unit_software_name = '"' + card.software_name + '"'
            context['unit_software_name'] = unit_software_name
            context['spacer_6'] = self.create_spacers((67,), (unit_software_name,))[0] * ' '
            unit_software_revision = '"' + card.software_revision + '"'
            context['unit_software_revision'] = unit_software_revision
            context['spacer_7'] = self.create_spacers((67,), (unit_software_revision,))[0] * ' '
            text = self._render('hardware_and_software', *scopes, context=context)
            self._write(text)

        elif self._validate((args[0],), 'CurrentStatus') and context['path'].split('/')[-1] == 'main':
            unit_state = card.state
            context['unit_state'] = unit_state
            context['spacer_1'] = self.create_spacers((67,), (unit_state,))[0] * ' '
            unit_hardware = '"' + card.board_name + ' ' + card.supplier_build_state + '"'
            context['unit_hardware'] = unit_hardware
            context['spacer_2'] = self.create_spacers((67,), (unit_hardware,))[0] * ' '
            unit_software = '"' + card.software[:-4] + '"'
            context['unit_software'] = unit_software
            context['spacer_3'] = self.create_spacers((67,), (unit_software,))[0] * ' '
            unit_serial_number = '"' + card.serial_number + '"'
            context['unit_serial_number'] = unit_serial_number
            context['spacer_4'] = self.create_spacers((67,), (unit_serial_number,))[0] * ' '
            unit_manufacturer_name = '"' + card.manufacturer_name + '"'
            context['unit_manufacturer_name'] = unit_manufacturer_name
            context['spacer_5'] = self.create_spacers((67,), (unit_manufacturer_name,))[0] * ' '
            unit_model_name = '"' + card.model_name + '"'
            context['unit_model_name'] = unit_model_name
            context['spacer_6'] = self.create_spacers((67,), (unit_model_name,))[0] * ' '
            text = self._render('current_status', *scopes, context=context)
            self._write(text)

        elif self._validate((args[0],), 'EquipmentInventory') and context['path'].split('/')[-1] == 'main':
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
