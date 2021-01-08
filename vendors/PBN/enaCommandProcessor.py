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
from .baseCommandProcessor import BaseCommandProcessor


class EnaCommandProcessor(BaseCommandProcessor):
    def do_exit(self, command, *args, context=None):
        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_conf(self, command, *args, context=None):
        from .confCommandProcessor import ConfCommandProcessor
        if args == ():
                subprocessor = self._create_subprocessor(ConfCommandProcessor, 'login', 'mainloop', 'ena', 'conf')
                subprocessor.loop(context=context)
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_wr(self, command, *args, context=None):
        if args == ():
            # TODO: Functionality
            print('hi')
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_copy(self, command, *args, context=None):
        if self._validate(command, 'startup-config', str):
            addr, = self._dissect(args, 'startup-config', str)
            # TODO: Functionality
        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)

    def do_show(self, command, *args, context=None):
        if self._validate(args, 'interface', str, str):
            ftth_version, port_name = self._dissect(args, 'interface', str, str)
            if ftth_version == 'ePON':
                expected_product = 'ftth-pon'
                context['port_name_prefix'] = 'EPON'
            elif ftth_version == 'gigaEthernet':
                expected_product = 'ftth'
                context['port_name_prefix'] = 'GigaEthernet'
            else:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            try:
                port = self._model.get_port('name', port_name)
                card = self._model.get_card('id', port.card_id)
                assert card.product == expected_product
            except exceptions.SoftboxenError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                                                       ('login', 'mainloop', 'ena'))
            except AssertionError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            _, port_index = port.name.split('/')
            context['port_index'] = port_index
            self.map_states(port, 'port')
            text = self._render('show_interface_product_port', context=dict(context, port=port))
            self._write(text)

        elif self._validate(args, 'running-config', 'interface', str, str):
            ftth_version, port_name = self._dissect(args, 'running-config', 'interface', str, str)
            if ftth_version == 'ePON':
                expected_product = 'ftth-pon'
                context['port_name_prefix'] = 'EPON'
            elif ftth_version == 'gigaEthernet':
                expected_product = 'ftth'
                context['port_name_prefix'] = 'GigaEthernet'
            else:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            try:
                port = self._model.get_port('name', port_name)
                card = self._model.get_card('id', port.card_id)
                assert card.product == expected_product
            except exceptions.SoftboxenError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                                                       ('login', 'mainloop', 'ena'))
            except AssertionError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('show_running-config_interface_product_port_top', context=dict(context, port=port))

            mid_text = ''
            if expected_product == "ftth-pon":
                try:
                    _ = self._model.get_ont("port_id", port.id)
                except exceptions.SoftboxenError:
                    pass
                else:
                    counter = 1
                    onts = self._model.get_onts("port_id", port.id)
                    for ont in onts:
                        if counter > 32:
                            mid_text = ''
                            break
                        context['counter'] = counter
                        mid_text = self._render('show_running-config_interface_product_port_mid',
                                                context=dict(context, ont=ont))
                        counter += 1

            text += mid_text
            text += self._render('show_running-config_interface_product_port_bottom', context=dict(context, port=port))
            self._write(text)

        elif self._validate(args, 'mac', 'address-table', 'interface', str, str):
            ftth_version, port_name = self._dissect(args, 'mac', 'address-table', 'interface', str, str)
            bottom_text = ""
            counter = 0
            context['spacer_1'] = self.create_spacers((4,), ('',))[0] * ' '
            context['spacer_2'] = self.create_spacers((4,), ('',))[0] * ' '

            if ftth_version == 'ePON':
                expected_product = 'ftth-pon'
            elif ftth_version == 'gigaEthernet':
                expected_product = 'ftth'
            else:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            try:
                port = self._model.get_port('name', port_name)
                card = self._model.get_card('id', port.card_id)
                assert card.product == expected_product
            except exceptions.SoftboxenError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandExecutionError(command=command, template='parameter_error', template_scopes=
                                                       ('login', 'mainloop', 'ena'))
            except AssertionError:
                full_command = command
                for arg in args:
                    full_command += ' ' + arg
                context['full_command'] = full_command
                raise exceptions.CommandSyntaxError(command=command)

            try:
                params = dict(connected_type='port', connected_id=port.id)
                service_ports = self._model.get_service_ports_by_values(params)
                for s_p in service_ports:
                    service_vlan = self._model.get_service_vlan('service_port_id', s_p.id)
                    vlan = self._model.get_vlan('id', service_vlan.vlan_id)
                    counter += 1
                    context['port_name'] = "g" + port.name
                    context['spacer_3'] = self.create_spacers((11,), (vlan.type,))[0] * ' '
                    bottom_text += self._render("show_mac_address_table_interface_product_port_bottom",
                                                context=dict(context, vlan=vlan))
            except exceptions.SoftboxenError:
                context['num_of_entries'] = counter
                text = self._render('show_mac_address_table_interface_product_port_top', context=context)
            else:
                context['num_of_entries'] = counter
                text = self._render('show_mac_address_table_interface_product_port_top', context=context)
                text += bottom_text

            self._write(text)

        else:
            full_command = command
            for arg in args:
                full_command += ' ' + arg
            context['full_command'] = full_command
            raise exceptions.CommandSyntaxError(command=command)
