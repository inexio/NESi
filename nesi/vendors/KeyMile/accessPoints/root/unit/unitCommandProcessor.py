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
from nesi.vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class UnitCommandProcessor(BaseCommandProcessor):
    __name__ = 'unit'
    management_functions = ('main', 'fm')
    access_points = ()  # 'internalPorts', only on certain cards

    from .unitManagementFunctions import main
    from .unitManagementFunctions import cfgm
    from .unitManagementFunctions import fm
    from .unitManagementFunctions import status

    def _init_access_points(self, context=None):
        self.access_points = ()
        try:
            card = self.get_component()

            self.management_functions = ('main', 'cfgm', 'fm', 'status')

            try:
                _ = self._model.get_logport('card_id', card.id)
            except exceptions.SoftboxenError:
                pass
            else:
                self.access_points += ('logports',)

            for port in self._model.get_ports('card_id', card.id):
                identifier = 'port-' + port.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

            for gport in self._model.get_portgroupports('card_id', card.id):
                identifier = 'portgroup-' + gport.name.split('/')[1][1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)
        except exceptions.InvalidInputError:
            pass

    def _init_context(self, context=None):
        try:
            card = self.get_component()
        except exceptions.SoftboxenError:
            context['ls_Name'] = ''
            context['ls_MainMode'] = ''
            context['ls_EquipmentState'] = 'Empty'
        else:
            context['ls_Name'] = card.board_name + ' ' + card.supplier_build_state
            context['ls_MainMode'] = card.software[:-4]
            context['ls_EquipmentState'] = 'Ok'

    def get_property(self, command, *args, context=None):
        try:
            card = self.get_component()
        except exceptions.InvalidInputError:
            if args[0] in ('CurrentStatus', 'EquipmentInventory'):
                card = None
            else:
                raise
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'SubscriberList') and context['path'].split('/')[-1] == 'status' and \
                (card.product == 'isdn' or card.product == 'analog'):
            text = self._render('subscriberList_top', *scopes, context=context)
            i = 0
            for subscriber in self._model.subscribers:
                if subscriber.registration_state == 'Unregistered':
                    context['i'] = i
                    context['spacer1'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                    context['spacer2'] = self.create_spacers((63,), (subscriber.registration_state,))[0] * ' '
                    context['spacer3'] = self.create_spacers((63,), (subscriber.address,))[0] * ' '

                    i += 1
                    text += self._render('subscriberList_item', *scopes, context=dict(context, subscriber=subscriber))
            text += self._render('subscriberList_bottom', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'SIP') and context['path'].split('/')[-1] == 'cfgm' and \
                (card.product == 'isdn' or card.product == 'analog'):
            context['spacer1'] = self.create_spacers((67,), (card.gateway_name,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.home_domain,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.sip_port_number,))[0] * ' '
            context['spacer4'] = self.create_spacers((65,), (card.country_code,))[0] * ' '
            context['spacer5'] = self.create_spacers((65,), (card.area_code,))[0] * ' '
            context['spacer6'] = self.create_spacers((67,), (card.retransmission_timer,))[0] * ' '
            context['spacer7'] = self.create_spacers((67,), (card.max_retransmission_interval,))[0] * ' '
            context['spacer8'] = self.create_spacers((67,), (card.sip_extension,))[0] * ' '
            context['spacer9'] = self.create_spacers((67,), (card.asserted_id_mode,))[0] * ' '
            context['spacer10'] = self.create_spacers((67,), (card.overlap_signalling,))[0] * ' '
            context['spacer11'] = self.create_spacers((67,), (card.overlap_timer,))[0] * ' '
            context['spacer12'] = self.create_spacers((67,), (card.uac_request_timer,))[0] * ' '
            context['spacer13'] = self.create_spacers((67,), (card.uas_request_timer,))[0] * ' '
            context['spacer14'] = self.create_spacers((67,), (card.session_expiration,))[0] * ' '
            text = self._render('sip', *scopes, context=dict(context, card=card))
            self._write(text)
        elif self._validate(args, 'Proxy') and context['path'].split('/')[-1] == 'cfgm' and \
                (card.product == 'isdn' or card.product == 'analog'):
            context['spacer1'] = self.create_spacers((67,), (card.proxy_mode,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.proxy_address,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.proxy_port,))[0] * ' '
            context['spacer4'] = self.create_spacers((67,), (card.proxy_address_sec,))[0] * ' '
            context['spacer5'] = self.create_spacers((67,), (card.proxy_port_sec,))[0] * ' '
            context['spacer6'] = self.create_spacers((67,), (card.proxy_enable,))[0] * ' '
            context['spacer7'] = self.create_spacers((67,), (card.proxy_method,))[0] * ' '
            context['spacer8'] = self.create_spacers((67,), (card.proxy_interval,))[0] * ' '
            text = self._render('proxy', *scopes, context=dict(context, card=card))
            self._write(text)
        elif self._validate(args, 'IP') and context['path'].split('/')[-1] == 'cfgm' and \
                (card.product == 'isdn' or card.product == 'analog'):
            context['spacer1'] = self.create_spacers((67,), (card.gateway_ipaddress,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.subnet_mask,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.default_gateway,))[0] * ' '
            text = self._render('ip', *scopes, context=dict(context, card=card))
            self._write(text)

        elif self._validate(args, 'Labels') and context['path'].split('/')[-1] == 'main':
            context['spacer1'] = self.create_spacers((67,), (card.label1,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.label2,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.description,))[0] * ' '
            text = self._render('labels', *scopes, context=dict(context, port=card))
            self._write(text)

        elif self._validate(args, 'Registrar') and context['path'].split('/')[-1] == 'cfgm':
            context['spacer1'] = self.create_spacers((67,), (card.registrar_adress,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (card.registrar_port,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (card.registration_mode,))[0] * ' '
            context['spacer4'] = self.create_spacers((67,), (card.registration_expiration_time,))[0] * ' '
            text = self._render('registrar', *scopes, context=dict(context, card=card))
            self._write(text)

        elif self._validate(args, 'HardwareAndSoftware') and context['path'].split('/')[-1] == 'main':
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

        elif self._validate(args, 'CurrentStatus') and context['path'].split('/')[-1] == 'main':
            if card is None:
                text = self._render('current_status_empty', *scopes, context=context)
            else:
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

        elif self._validate(args, 'EquipmentInventory') and context['path'].split('/')[-1] == 'main':
            if card is None:
                text = self._render('equipment_inventory_empty', *scopes, context=context)
            else:
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

    def get_component(self):
        return self._model.get_card('name', self.component_name)

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
        elif self._validate(args, 'Ip', str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            ip1, ip2, ip3 = self._dissect(args, 'Ip', str, str, str)
            try:
                component = self.get_component()
                component.set_ip(ip1, ip2, ip3)
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'SIP', str, str, str, str, str, str, str, str, str, str, str, str, str, str) and \
                context['path'].split('/')[-1] == 'cfgm' and (card.product == 'isdn' or card.product == 'analog'):
            gw, hd, spn, cc, ac, rt, mri, se, aim, os, ot, uac, uas, sessione = self._dissect(
                args, 'Sip', str, str, str, str, str, str, str, str, str, str, str, str, str, str)
            try:
                se = True if se.lower() == 'true' else False
                os = True if os.lower() == 'true' else False
                uac = True if uac.lower() == 'true' else False
                uas = True if uas.lower() == 'true' else False
                aim = None if aim.lower() == 'none' else aim

                card.set_sip(gw, hd, int(spn), cc, ac, int(rt), int(mri), se, aim, os, int(ot), uac, uas, int(sessione))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate((args[0],), 'Digitmap') and \
                context['path'].split('/')[-1] == 'cfgm' and (card.product == 'isdn' or card.product == 'analog'):
            pass
        elif self._validate(args, 'Registrar', str, str, str, str) and \
            context['path'].split('/')[-1] == 'cfgm' and (card.product == 'isdn' or card.product == 'analog'):
            ra, rp, rm, rt = self._dissect(args, 'Registrar', str, str, str, str)
            try:
                card.set_registrar(ra, int(rp), rm, int(rt))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args[:9], 'Proxy', str, str, str, str, str, str, str, str) and \
            context['path'].split('/')[-1] == 'cfgm' and (card.product == 'isdn' or card.product == 'analog'):
            pm, pa1, pp1, pa2, pp2, pe, pmethod, pi = self._dissect(args, 'Proxy', str, str, str, str, str, str, str, str)
            try:
                pe = True if pe.lower() == 'true' else False
                card.set_proxy(pm, pa1, int(pp1), pa2, int(pp2), pe, pmethod, int(pi))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_restart(self, command, *args, context=None):
        card = self.get_component()
        if len(args) == 0 and context['path'].split('/')[-1] == 'main' and (card.product == 'isdn' or card.product == 'analog'):
            time.sleep(10)
            exc = exceptions.TerminalExitError()
            exc.return_to = 'sysreboot'
            raise exc
        else:
            raise exceptions.CommandSyntaxError(command=command)
