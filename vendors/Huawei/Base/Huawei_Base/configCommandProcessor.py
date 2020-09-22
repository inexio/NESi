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
import random
import datetime
import re
import time

from nesi import exceptions
from .huaweiBaseCommandProcessor import HuaweiBaseCommandProcessor
from .baseMixIn import BaseMixIn
from .vlanSrvprofCommandProcessor import VlanSrvprofCommandProcessor


class ConfigCommandProcessor(HuaweiBaseCommandProcessor, BaseMixIn):

    def do_disable(self, command, *args, context=None):

        from .userViewCommandProcessor import UserViewCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = UserViewCommandProcessor
        raise exc

    def do_return(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = EnableCommandProcessor
        raise exc

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render(
                '?',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_backup(self, command, *args, context=None):
        if self._validate(args, 'configuration', 'tftp', str, str):
            ip, path = self._dissect(args, 'configuration', 'tftp', str, str)
            time.sleep(5)
            text = self._render('backup_configuration_tftp', context=context)
            self._write(text)
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_interface(self, command, *args, context=None):

        from .interfaceCommandProcessor import InterfaceCommandProcessor

        if self._validate(args, str, str):
            iftype, interface_id = self._dissect(args, str, str)

            if iftype == 'vlanif':
                vlan_if_name = 'vlanif' + interface_id
                try:
                    vlan = self._model.get_vlan('number', int(interface_id))
                except exceptions.SoftboxenError:
                    text = self._render('vlan_does_not_exist', context=context)
                    self._write(text)
                    return

                try:
                    component = self._model.get_vlan_interface("name", vlan_if_name)
                    check = True
                except exceptions.SoftboxenError:
                    self._model.add_vlan_interface(name=vlan_if_name, vlan_id=vlan.id)
                    component = self._model.get_vlan_interface('name', vlan_if_name)
                    check = True

            elif iftype == 'emu':
                try:
                    component = self._model.get_emu("number", int(interface_id))
                    check = True

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            elif iftype in ('adsl', 'gpon', 'opg', 'vdsl', 'eth'):
                try:
                    component = self._model.get_card("name", interface_id)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if iftype == 'gpon' and component.product == 'ftth-pon':
                    check = True
                elif iftype == 'opg' and component.product == 'ftth' and component.board_name == 'H802OPGE':
                    check = True
                elif iftype == 'eth' and component.product == 'ftth' and component.board_name != 'H802OPGE':
                    check = True
                elif iftype == 'vdsl' and component.product == 'vdsl':
                    check = True
                elif iftype == 'adsl' and component.product == 'adsl':
                    check = True
                else:
                    check = False
            else:
                raise exceptions.CommandSyntaxError(command=command)

            if check:
                subprocessor = self._create_subprocessor(
                    InterfaceCommandProcessor, 'login', 'mainloop', 'enable', 'config', 'interface')
                subprocessor.loop(context=dict(context, component=component, iftype=iftype),
                                  return_to=ConfigCommandProcessor)
            else:
                self._write(self._render('board_type_error', context=context))
                return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_display(self, command, *args, context=None):
        if self._validate(args, 'board', str):
            self.display_board(command, args, context)
        elif self._validate(args, 'ont', 'autofind', 'all'):
            autofind_onts = []

            for port in self._model.ports:
                if port.ont_autofind:
                    onts = self._model.get_onts('port_id', port.id)
                    for ont in onts:
                        autofind_onts.append(ont)

            for autofind_ont in autofind_onts:
                port = self._model.get_port('id', autofind_ont.port_id)
                context['port_identifier'] = port.name
                context['ont'] = autofind_ont
                self._write(self._render('display_ont_autofind_all_body', context=context))

            if len(autofind_onts) == 0:
                self._write(self._render('display_ont_autofind_all_failure', context=context))
                return

            context['autofind_count'] = len(autofind_onts)
            self._write(self._render('display_ont_autofind_all_footer', context=context))
        elif self._validate(args, 'ont', 'info', 'summary', str):
            def generate_ont_info_summary(port):
                text = ''
                text_middle = ''
                text_middle2 = ''
                context['ont_count'] = 0
                context['ont_online_count'] = 0
                context['port_identifier'] = port.name
                onts = self._model.get_onts('port_id', port.id)
                distance = random.randint(0, 7) * 1000
                for ont in onts:
                    self.map_states(ont, 'ont')
                    context['ont_count'] += 1
                    if ont.admin_state == 'online':
                        context['ont_online_count'] += 1
                    context['ont_idx'] = ont.name.split("/")[-1]
                    context['ont_serial_number'] = ont.serial_number
                    context['ont_description'] = ont.description
                    context['ont_distance'] = random.randint(distance, distance + 1000)
                    context['rx_power'] = round(random.uniform(15, 25), 2)
                    context['tx_power'] = round(random.uniform(1, 3), 2)
                    context['ont_admin_state'] = ont.admin_state
                    date = datetime.date.today() - datetime.timedelta(days=random.randint(7, 28))
                    if ont.admin_state == 'online':
                        context['last_uptime'] = date.strftime('%Y-%m-%d %H:%M:%S')
                        context['last_downtime'] = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        context['last_uptime'] = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                        context['last_downtime'] = date.strftime('%Y-%m-%d %H:%M:%S')
                    text_middle += self._render('display_ont_info_summary_0_middle', context=context)
                    text_middle2 += self._render('display_ont_info_summary_0_middle2', context=context)

                text += self._render('display_ont_info_summary_0_top', context=context)
                text += text_middle
                text += self._render('display_ont_info_summary_0_top2', context=context)
                text += text_middle2
                text += self._render('display_ont_info_summary_0_bottom', context=context)

                return text

            identifier, = self._dissect(args, 'ont', 'info', 'summary', str)

            components = identifier.split("/")
            self._write('  Command is being executed. Please wait\n')
            text = ''
            if len(components) == 1:
                try:
                    subrack = self._model.get_subrack('name', identifier)
                except exceptions.InvalidInputError:
                    self.on_error(context=context)
                    return
                cards = self._model.get_cards('subrack_id', subrack.id)
                for card in cards:
                    if card.product not in ('ftth-pon', 'ftth'):
                        continue
                    ports = self._model.get_ports('card_id', card.id)
                    for port in ports:
                        text += generate_ont_info_summary(port)
            elif len(components) == 2:
                try:
                    card = self._model.get_card('name', identifier)
                except exceptions.InvalidInputError:
                    self.on_error(context=context)
                    return
                if card.product not in ('ftth-pon', 'ftth'):
                    self._write(self._render('operation_not_supported_by_board_failure', context=context))
                    return
                ports = self._model.get_ports('card_id', card.id)
                for port in ports:
                    text += generate_ont_info_summary(port)
            elif len(components) == 3:
                try:
                    port = self._model.get_port('name', identifier)
                except exceptions.InvalidInputError:
                    self.on_error(context=context)
                    return
                card = self._model.get_card('id', port.card_id)
                if card.product not in ('ftth-pon', 'ftth'):
                    self._write(self._render('operation_not_supported_by_port_failure', context=context))
                    return
                text += generate_ont_info_summary(port)
            else:
                raise exceptions.CommandSyntaxError

            self._write(text)
        elif self._validate(args, 'interface', 'vlanif', str):
            vlan_number, = self._dissect(args, 'interface', 'vlanif', str)
            name = 'vlanif' + vlan_number
            try:
                vlanif = self._model.get_vlan_interface("name", name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('display_interface_vlanif_num', context=dict(context, vlanif=vlanif))
            self._write(text)
        elif self._validate(args, 'vlan', 'all'):
            if self._model.interactive_mode:
                self.user_input('{ <cr>|vlanattr<K>|vlantype<E><mux,standard,smart> }:')
            text = self._render('display_vlan_all_top', context=context)
            count = 0
            for vlan in self._model.vlans:
                portnum = 0
                servportnum = 0
                for port in self._model.ports:
                    if port.vlan_id == vlan.number:
                        portnum += 1
                for sport in self._model.service_vlans:
                    if sport.vlan_id == vlan.id:
                        servportnum += 1

                context['portnum'] = portnum
                context['servportnum'] = servportnum
                context['spacer1'] = self.create_spacers((6,), (vlan.number,))[0] * ' '
                context['spacer2'] = self.create_spacers((10,), (vlan.type,))[0] * ' '
                context['spacer3'] = self.create_spacers((23,), (vlan.attribute,))[0] * ' '
                context['spacer4'] = self.create_spacers((16,), (len(str(servportnum)),))[0] * ' '
                context['spacer5'] = ' '
                text += self._render('display_vlan_all_mid', context=dict(context, vlan=vlan))
                count += 1

            text += self._render('display_vlan_all_bottom', context=dict(context, count=count))
            self._write(text)

        elif self._validate(args, 'version'):
            if self._model.interactive_mode:
                self.user_input('{ <cr>|backplane<K>|frameid/slotid<S><Length 1-15> }:')
            text = self._render('display_version', context=dict(context, box=self._model))
            self._write(text)

        elif self._validate(args, 'alarm', 'active', 'alarmtype', 'environment', 'detail'):
            text = self._render('display_alarm_active_alarmtype_environment_detail', context=context)
            self._write(text)

        elif self._validate(args, 'pitp', 'config'):
            text = self._render(
                'display_pitp_config',
                context=dict(context, box=self._model))
            self._write(text)

        elif self._validate(args, 'mac-address', 'all'):
            if self._model.interactive_mode:
                self.user_input('{ <cr>||<K> }:')

            self._write('  It will take some time, please wait...\n')

            text = self._render('display_mac_address_all_top', context=context)

            mac_address_count = 0
            for cpe in self._model.cpes:
                port = None
                ont_port = None
                if cpe.port_id is not None:
                    port = self._model.get_port('id', cpe.port_id)
                elif cpe.ont_port_id is not None:
                    ont_port = self._model.get_ont_port('id', cpe.ont_port_id)
                else:
                    pass
                    #TODO: Raise exception: Floating CPE found

                ont = None
                if port is None:
                    ont = self._model.get_ont('id', ont_port.ont_id)
                    port = self._model.get_port('id', ont.port_id)

                card = self._model.get_card('id', port.card_id)

                if card.product == 'adsl':
                    context['product'] = 'adl '
                elif card.product == 'vdsl':
                    context['product'] = 'vdl '
                elif card.product == 'ftth':
                    context['product'] = 'eth '
                elif card.product == 'ftth-pon':
                    context['product'] = 'gpon'

                ont_identifier = None
                ont_port_identifier = None

                if ont_port is None:
                    subrack_identifier, card_identifier, port_identifier = port.name.split('/')
                else:
                    subrack_identifier, card_identifier, port_identifier, ont_identifier, ont_port_identifier = \
                        ont_port.name.split('/')

                context['subrack'] = subrack_identifier
                context['card'] = card_identifier
                context['port'] = port_identifier
                if ont is None:
                    context['ont'] = '-'
                else:
                    context['ont'] = ont_identifier
                if ont_port is None:
                    context['ont_port'] = '-'
                else:
                    context['ont_port'] = ont_port_identifier
                context['cpe_mac'] = cpe.mac
                text += self._render('display_mac_address_all_middle', context=context)
                mac_address_count += 1

            context['mac_address_count'] = mac_address_count
            text += self._render('display_mac_address_all_bottom', context=context)

            self._write(text)

        elif self._validate(args, 'current-configuration', 'section', 'vlan-srvprof'):
            if self._model.interactive_mode:
                self.user_input('{ <cr>||<K> }:')
            text = self._render('display_current_configuration_section_vlan_srvprof_top',
                                context=dict(context, box=self._model))
            text2 = ''
            for vlan in self._model.vlans:
                try:
                    if vlan.bind_service_profile_id is not None and int(vlan.bind_service_profile_id) >= 0:
                        text2 += self._render('display_current_configuration_section_vlan_srvprof_bot',
                                              context=dict(context, vlan=vlan))
                except ValueError:
                    raise exceptions.CommandSyntaxError(command=command)

            for profile in self._model.port_profiles:
                if profile.type == 'service':
                    text += self._render('display_current_configuration_section_vlan_srvprof_mid',
                                         context=dict(context, profile=profile))

            text += text2
            text += self._render('display_current_configuration_section_vlan_srvprof_bot2',
                                 context=context)
            self._write(text)

        elif self._validate(args, 'service-port', str):
            self.display_service_port(command, args, context)

        elif self._validate(args, 'emu'):
            input = self.user_input('{ <cr>|emuid<U><0,15>|monitor-server<K> }:')
            if input == '':
                text = ''
                liste = []
                for emu in self._model.emus:
                    name = 'emu' + str(emu.number)
                    spacername1 = 'spacer' + str(emu.number * 2 + 1)
                    spacername2 = 'spacer' + str(emu.number * 2 + 2)
                    context[spacername1] = self.create_spacers((19,), (emu.type,))[0] * ' '
                    context[spacername2] = self.create_spacers((12,), (emu.emu_state,))[0] * ' '
                    liste.append(emu.number)
                    context[name] = emu
                text += self._render('display_emu', context=dict(context, liste=liste))
                self._write(text)
            try:
                if int(input) <= 15:
                    try:
                        emu = self._model.get_emu("number", int(input))
                    except exceptions.SoftboxenError:
                        raise exceptions.CommandSyntaxError(command=command)
                    text = self._render('display_emu_id', context=dict(context, emu=emu))
                    self._write(text)

            except ValueError:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'emu', str):
            emu_number, = self._dissect(args, 'emu', str)
            try:
                emu = self._model.get_emu("number", int(emu_number))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            text = self._render('display_emu_id', context=dict(context, emu=emu))
            self._write(text)

        elif self._validate(args, 'terminal', 'user', 'all'):
            self.display_terminal_user(command, context)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_service_port(self, command, *args, context=None):
        if args[3] == 'vdsl':
            port_idx = args[6]
        else:
            port_idx = args[4]
        try:
            port = self._model.get_port('name', port_idx)
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)
        if args[5] == 'ont':
            ont_idx = args[6]
            ont_port_idx = args[8]
            try:
                ont_name = port.name + '/' + ont_idx
                ont = self._model.get_ont('name', ont_name)
                ont_port_name = ont.name + '/' + ont_port_idx
                ont_port = self._model.get_ont_port('name', ont_port_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            connected_id = ont_port.id
            connected_type = 'ont'
        else:
            connected_id = port.id
            connected_type = 'port'

        s_port_id = args[0]
        params = dict(name=s_port_id)
        service_port = self._model.get_service_port_by_values(params)
        if service_port is not None:
            text = self._render('service_port_does_already_exist', context=dict(context, service_port=service_port))
            self._write(text)
            return
        self._model.add_service_port(name=s_port_id, connected_id=connected_id, connected_type=connected_type)
        service_port = self._model.get_service_port('name', s_port_id)

        vlan_id = args[2]
        try:
            vlan = self._model.get_vlan('number', int(vlan_id))
        except exceptions.SoftboxenError:
            service_port.delete()
            text = self._render('vlan_does_not_exist', context=context)
            self._write(text)
            return

        self._model.add_service_vlan(name=vlan_id, vlan_id=vlan.id, service_port_id=service_port.id)
        service_vlan = self._model.get_service_vlan('service_port_id', service_port.id)

        if self._validate(args, str, 'vlan', str, 'adsl', str, 'vpi', str, 'vci', str, 'multi-service', 'user-encap',
                          'pppoe', 'inbound', 'traffic-table', 'index', str, 'outbound', 'traffic-table', 'index',
                          str):
            s_port_idx, vlan_idx, port_idx, vpi, vci, table_in, table_out = \
                self._dissect(args, str, 'vlan', str, 'adsl', str, 'vpi', str, 'vci', str, 'multi-service',
                              'user-encap', 'pppoe', 'inbound', 'traffic-table', 'index', str, 'outbound',
                              'traffic-table', 'index', str)

            try:
                card = self._model.get_card('id', port.card_id)
                assert card.product == 'adsl'
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_vci(vci)
            service_port.set_vpi(vpi)
            service_port.set_inbound_table_name(table_in)
            service_port.set_outbound_table_name(table_out)

        elif self._validate(args, str, 'vlan', str, 'vdsl', 'mode', 'atm', str, 'vpi', str, 'vci', str,
                            'multi-service', 'user-encap', 'pppoe', 'inbound', 'traffic-table', 'index', str,
                            'outbound', 'traffic-table', 'index', str):
            _, _, _, vpi, vci, table_in, table_out = \
                self._dissect(args, str, 'vlan', str, 'vdsl', 'mode', 'atm', str, 'vpi', str, 'vci', str,
                              'multi-service', 'user-encap', 'pppoe', 'inbound', 'traffic-table', 'index', str,
                              'outbound', 'traffic-table', 'index', str)

            try:
                card = self._model.get_card('id', port.card_id)
                assert (card.product == 'vdsl') or (card.product == 'xdsl')
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_vci(vci)
            service_port.set_vpi(vpi)
            service_port.set_inbound_table_name(table_in)
            service_port.set_outbound_table_name(table_out)
            service_vlan.set_mode('ptm')

        elif self._validate(args, str, 'vlan', str, 'vdsl', 'mode', 'ptm', str, 'multi-service', 'user-encap', 'pppoe',
                            'inbound', 'traffic-table', 'index', str, 'outbound', 'traffic-table', 'index', str):
            _, _, _, table_in, table_out = self._dissect(args, str, 'vlan', str, 'vdsl', 'mode', 'ptm', str,
                                                         'multi-service', 'user-encap', 'pppoe', 'inbound',
                                                         'traffic-table', 'index', str, 'outbound', 'traffic-table',
                                                         'index', str)
            try:
                card = self._model.get_card('id', port.card_id)
                assert (card.product == 'vdsl') or (card.product == 'xdsl')
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_inbound_table_name(table_in)
            service_port.set_outbound_table_name(table_out)
            service_vlan.set_mode('atm')

        elif self._validate(args, str, 'vlan', str, 'eth', str, 'multi-service', 'user-vlan', str, 'user-encap',
                            'pppoe', 'inbound', 'traffic-table', 'index', str, 'outbound', 'traffic-table',
                            'index', str):
            _, vlan_1, _, vlan_2, table_in, table_out = self._dissect(args, str, 'vlan', str, 'eth', str,
                                                                      'multi-service', 'user-vlan', str, 'user-encap',
                                                                      'pppoe', 'inbound', 'traffic-table', 'index', str,
                                                                      'outbound', 'traffic-table', 'index', str)

            if vlan_1 != vlan_2:
                service_vlan.delete()
                service_port.delete()
                return

            try:
                card = self._model.get_card('id', port.card_id)
                assert card.product == 'ftth'
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_inbound_table_name(table_in)
            service_port.set_outbound_table_name(table_out)

        elif self._validate(args, str, 'vlan', str, 'vdsl', 'mode', 'ptm', str, 'multi-service', 'user-vlan',
                            'untagged'):
            try:
                card = self._model.get_card('id', port.card_id)
                assert card.product == 'vdsl'
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_vlan.set_tag('untagged')
            service_vlan.set_mode('ptm')
            vlan.set_tag('untagged')

        elif self._validate(args, str, 'vlan', str, 'vdsl', 'mode', 'atm', str, 'vpi', str, 'vci', str,
                            'multi-service', 'user-vlan', 'untagged'):
            _, _, _, vpi, vci = self._dissect(args, str, 'vlan', str, 'vdsl', 'mode', 'atm', str, 'vpi', str, 'vci',
                                              str, 'multi-service', 'user-vlan', 'untagged')
            try:
                card = self._model.get_card('id', port.card_id)
                assert (card.product == 'adsl') or (card.product == 'xdsl')
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_vpi(vpi)
            service_port.set_vci(vci)
            service_vlan.set_mode('atm')

        elif self._validate(args, str, 'vlan', str, 'port', str, 'ont', str, 'eth', str, 'multi-service', 'user-vlan',
                            'untagged', 'tag-transform', 'default', 'inbound', 'traffic-table', 'index', str,
                            'outbound', 'traffic-table', 'index', str):
            _, _, _, ont_idx, ont_port_idx, inbound_table, outbound_table = \
                self._dissect(args, str, 'vlan', str, 'port', str, 'ont', str, 'eth', str, 'multi-service', 'user-vlan',
                              'untagged', 'tag-transform', 'default', 'inbound', 'traffic-table', 'index', str,
                              'outbound', 'traffic-table', 'index', str)

            try:
                card = self._model.get_card('id', port.card_id)
                assert card.product == 'ftth-pon'
            except (exceptions.SoftboxenError, AssertionError):
                service_vlan.delete()
                service_port.delete()
                raise exceptions.CommandSyntaxError(command=command)

            service_port.set_inbound_table_name(inbound_table)
            service_port.set_outbound_table_name(outbound_table)

        else:
            service_vlan.delete()
            service_port.delete()
            raise exceptions.CommandSyntaxError(command=command)

    def do_ntp_service(self, command, *args, context=None):
        if self._validate(args, 'unicast-server', str):
            addr, = self._dissect(args, 'unicast-server', str)
            try:
                assert addr.count('.') == 3
                for i in addr.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
            self._model.set_sntp_server_ip_address(addr)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_timezone(self, command, *args, context=None):
        if self._validate(args, str, str):
            timezone, offset = self._dissect(args, str, str)
            self._model.set_timezone_offset(timezone + '' + offset)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_time(self, command, *args, context=None):
        if self._validate(args, 'dst', 'start', str, 'last', 'Sun', str, 'end', str, 'last', 'Sun', str,
                          'adjust', str):
            # we dont have some internal time to set
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vlan(self, command, *args, context=None):
        if self._validate(args, 'bind', 'service-profile', str, 'profile-id', str):
            trafficvlan, id = self._dissect(args, 'bind', 'service-profile', str, 'profile-id', str)
            try:
                profile = self._model.get_port_profile('internal_id', int(id))
                assert profile.box_id == self._model.id
                assert profile.type == "service"
            except (exceptions.InvalidInputError, AssertionError):
                self._write(self._render('vlan_service_profile_does_not_exist', context=context))
                return
            try:
                vlan = self._model.get_vlan("number", int(trafficvlan))
            except exceptions.InvalidInputError:
                self._write(self._render('vlan_does_not_exist', context=context))
                return

            vlan.set_service_profile_id(int(profile.id))
            text = self._render(
                'vlan_bind_service-profile_vlan-id_profile-id_profile-id',
                context=context)
            self._write(text)

        elif self._validate(args, 'service-profile', 'profile-name', str, 'profile-id', str):
            name, id = self._dissect(args, 'service-profile', 'profile-name', str, 'profile-id', str)
            try:
                profile = self._model.get_port_profile('internal_id', int(id))
                assert profile.type == "service"
            except exceptions.SoftboxenError:
                try:
                    self._model.add_port_profile(name=name, type='service', internal_id=id)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            except AssertionError:
                raise exceptions.CommandSyntaxError(command=command)
            try:
                profile = self._model.get_port_profile('internal_id', int(id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['srvprof'] = profile
            subprocessor = self._create_subprocessor(
                VlanSrvprofCommandProcessor, 'login', 'mainloop', 'enable', 'config', 'srvprof')

            subprocessor.loop(context=context, return_to=ConfigCommandProcessor)

        elif self._validate(args, str, 'smart'):
            trafficvlan, = self._dissect(args, str, 'smart')
            try:
                vlan = self._model.get_vlan("number", int(trafficvlan))
            except exceptions.SoftboxenError:
                self._model.add_vlan(number=int(trafficvlan), name='VLAN_' + trafficvlan)
                try:
                    vlan = self._model.get_vlan("number", int(trafficvlan))
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                return

            text = self._render('vlan_already_exists', context=context)
            self._write(text)
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio_format(self, command, *args, context=None):
        # not needed in simulation
        if self._validate(args, 'pitp-pmode', 'cid', 'eth', '"anid', 'eth', 'slot/port+1"'):
            return

        elif self._validate(args, 'pitp-pmode', 'cid', 'atm', '"anid', 'atm', 'slot/port+1:vpi:vci"'):
            return

        elif self._validate(args, 'pitp-pmode', 'rid', 'plabel'):
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio(self, command, *args, context=None):
        # not needed in simulation
        if self._validate(args, 'sub-option', '0x81', 'pitp-pmode', 'enable'):
            return

        elif self._validate(args, 'sub-option', '0x81', 'pitp-pmode', 'disable'):
            return

        elif self._validate(args, 'sub-option', '0x82', 'pitp-pmode', 'enable'):
            return

        elif self._validate(args, 'sub-option', '0x82', 'pitp-pmode', 'disable'):
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pitp(self, command, *args, context=None):
        if self._validate(args, str, str):
            pitp, mode = self._dissect(args, str, str)
            if pitp == 'enable' or pitp == 'disable':
                self._model.set_pitp(pitp)
                self._model.set_pitp_mode(mode)
                text = self._render('pitp_enable_pmode', context=context)
                self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio_mode(self, command, *args, context=None):
        if self._validate(args, 'user-defined', 'pitp-pmode'):
            # not needed in simulation
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio_anid(self, command, *args, context=None):
        if self._validate(args, str):
            ip, = self._dissect(args, str)

            try:
                assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip)
                assert ip.count('.') == 3
                for i in ip.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            box = self._model
            box.set_raio_anid(ip)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_undo(self, command, *args, context=None):
        if self._validate(args, 'system', 'snmp-user', 'password', 'security'):
            # importend for future snmp interactions
            return
        elif self._validate(args, 'service-port', str):
            s_port_idx, = self._dissect(args, 'service-port', str)

            try:
                s_port = self._model.get_service_port('name', s_port_idx)
                s_vlan = self._model.get_service_vlan('service_port_id', s_port.id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            s_port.delete()
            s_vlan.delete()

        elif self._validate(args, 'smart'):
            self._write("  Interactive function is disabled\n")
            self._model.disable_interactive()
        elif self._validate(args, 'interactive'):
            return

        elif self._validate(args, 'ip', 'route-static', 'all'):
            answer = self.user_input('Are you sure? [Y/N]:')
            if answer != 'Y':
                return

            for route in self._model.routes:
                route.delete()

        elif self._validate(args, 'interface', 'vlanif', str):
            vlanif_num, = self._dissect(args, 'interface', 'vlanif', str)
            try:
                v_if_name = 'vlanif' + vlanif_num
                vlan_if = self._model.get_vlan_interface('name', v_if_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            vlan_if.delete()

        elif self._validate(args, 'port', 'vlan', str, str, str):
            vlan_idx, card_idx, port_id = self._dissect(args, 'port', 'vlan', str, str, str)
            try:
                vlan = self._model.get_vlan('number', int(vlan_idx))
                card = self._model.get_card('name', card_idx)
                port_name = card_idx + '/' + port_id
                port = self._model.get_port('name', port_name)
                service_vlan = self._model.get_service_vlan('vlan_id', vlan.id)
                service_port = self._model.get_service_port('connected_id', port.id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if service_vlan.service_port_id != service_port.id:
                raise exceptions.CommandSyntaxError(command=command)

            service_port.delete()
            service_vlan.delete()

        elif self._validate(args, 'vlan', str):
            vlan_idx, = self._dissect(args, 'vlan', str)

            try:
                vlan = self._model.get_vlan('number', int(vlan_idx))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            try:
                vlan_if = self._model.get_vlan_interface('vlan_id', vlan.id)
            except exceptions.SoftboxenError:
                vlan.delete()
                return

            text = self._render('delete_vlan_if_first', context=context)
            self._write(text)
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_snmp_agent(self, command, *args, context=None):
        # importend for future snmp interactions
        if self._validate(args, 'community', 'read', str):
            return
        elif self._validate(args, 'community', 'write', str):
            return
        elif self._validate(args, 'target-host', 'trap-hostname', str, 'address', str,
                            'udp-port', str , 'trap-paramsname', str):
            return
        elif self._validate(args, 'target-host', 'trap-paramsname', str, 'v1', 'securityname',
                            str):
            return
        elif self._validate(args, 'trap', 'enable', 'standard'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_system(self, command, *args, context=None):
        if self._validate(args, 'handshake', 'interval', str):
            interval, = self._dissect(args, 'handshake', 'interval', str)
            self._model.set_handshake_interval(interval)
        elif self._validate(args, 'handshake', str):
            mode, = self._dissect(args, 'handshake', str)
            if mode == 'enable' or mode == 'disable':
                self._model.set_handshake_mode(mode)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_terminal(self, command, *args, context=None):
        if self._validate(args, 'user', 'name'):
            login = self.user_input("  User Name(length<6,15>):", False, 15)

            try:
                usr = self._model.get_user('name', login)
            except exceptions.SoftboxenError:
                pass
            else:
                context['user_name'] = login
                text = self._render('user_already_exists', context=context)
                self._write(text)
                self.line_buffer = []  # manually clear buffer in case of 'Exception'
                return
            while len(login) < 6:
                text = self._render('terminal_name_short', context=context)
                self._write(text)
                login = self.user_input("  User Name(length<6,15>):", False, 15)

            self.hide_input = True
            password = self.user_input("  User Password(length<6,15>):", False, 15)
            while len(password) < 6:
                text = self._render('terminal_pw_short', context=context)
                self._write(text)
                password = self.user_input("  User Password(length<6,15>):", False, 15)

            password_repeat = self.user_input("  Confirm Password(length<6,15>):", False)
            while password != password_repeat:
                text = self._render('terminal_pw_error', context=context)
                self._write(text)
                password_repeat = self.user_input("  Confirm Password(length<6,15>):", False, 15)
            self.hide_input = False

            profile = self.user_input("  User profile name(<=15 chars)[root]:", False, 15)
            while (profile != 'root') and (profile != 'admin') and (profile != 'operator') \
                    and (profile != 'commonuser'):
                text = self._render('terminal_profile_error', context=context)
                self._write(text)
                profile = self.user_input("  User profile name(<=15 chars)[root]:", False, 15)

            text = self._render('user_level', context=context)
            self._write(text)
            level = self.user_input("     1. Common User  2. Operator  3. Administrator:", False)
            while (level != '1') and (level != '2') and (level != '3'):
                text = self._render('terminal_level_error', context=context)
                self._write(text)
                text = self._render('user_level', context=context)
                self._write(text)
                level = self.user_input("     1. Common User  2. Operator  3. Administrator:", False)

            if level == '1':
                lvl = 'User'
            elif level == '2':
                lvl = 'Operator'
            elif level == '3':
                lvl = 'Admin'
            else:
                raise exceptions.CommandSyntaxError(command=command)

            reenter_num = self.user_input("  Permitted Reenter Number(0--20):", False, 2)
            while (int(reenter_num) < 0) or (int(reenter_num) > 20):
                text = self._render('terminal_error_choice', context=context)
                self._write(text)
                reenter_num = self.user_input("  Permitted Reenter Number(0--20):", False, 2)

            info = self.user_input("  User's Appended Info(<=30 chars):", False, 30)

            box = self._model
            box.add_credentials(username=login, password=password)
            try:
                creds = self._model.get_credentials('username', login)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            box.add_user(name=login, credentials_id=creds.id, level=lvl, profile=profile, reenter_num=reenter_num,
                         reenter_num_temp=reenter_num, append_info=info, lock_status='Unlocked')
            try:
                user = self._model.get_user('name', login)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('user_created', context=context)
            self._write(text)

            var_n = self.user_input("  Repeat this operation? (y/n)[n]:", False, 1)
            if var_n == 'y':
                self.do_terminal(command, 'user', 'name', context=context)
                return
            elif var_n == 'n':
                return

        elif self._validate(args, 'unlock', 'user', str):
            user_name, = self._dissect(args, 'unlock', 'user', str)

            try:
                locked_user = self._model.get_user('name', user_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if locked_user.lock_status == 'Locked':
                locked_user.set_reenter_num_temp(locked_user.reenter_num)
                locked_user.unlock()
                return
            elif locked_user.lock_status == 'Unlocked':
                text = self._render('user_already_unlocked', context=context)
                self._write(text)
            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_port(self, command, *args, context=None):
        if self._validate(args, 'vlan', str, str, str):
            trafficvlan, cardident, portid = self._dissect(args, 'vlan', str, str, str)
            portident = cardident + '/' + portid
            try:
                card = self._model.get_card('name', cardident)
                if card.product != 'mgnt':
                    self._write(self._render('operation_not_supported_by_board', context=context))
                    return
                port = self._model.get_port("name", portident)
                vlan = self._model.get_vlan("number", int(trafficvlan))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if port.vlan_id == vlan.number:
                self._write(self._render('port_already_in_vlan', context=context))
                return

            port.set_vlan_id(vlan.number)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_xdsl(self, command, *args, context=None):
        if self._validate(args, 'vectoring-group', 'link', 'add', str, str):
            profile_idx, port_idx = self._dissect(args, 'vectoring-group', 'link', 'add', str, str)
            print(port_idx)
            portname = port_idx[0:3] + '/' + port_idx[4]

            try:
                port = self._model.get_port("name", portname)
                port.set_vectoring_group(int(profile_idx))

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            return

        elif self._validate(args, 'vectoring-group', 'link', 'delete', str, str):
            profile_idx, port_idx = self._dissect(args, 'vectoring-group', 'link', 'delete', str, str)
            portname = str(port_idx[0:3] + '/' + port_idx[4])
            try:
                port = self._model.get_port("name", portname)
                assert int(port.vectoring_group) == int(profile_idx)
                port.set_vectoring_group(None)

            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            return

        elif self._validate(args[:3], 'data-rate-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'data-rate-profile', 'quickadd', str)
            name = 'data_rate_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='data-rate')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return

            self.data_rate_profile_setup(port_profile, args, command)

        elif self._validate(args[:3], 'data-rate-profile', 'quickmodify', str):
            profile_num, = self._dissect(args[:3], 'data-rate-profile', 'quickmodify', str)
            name = 'data_rate_' + profile_num
            try:
                port_profile = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                text = self._render('port_profile_does_not_exist', context=context)
                self._write(text)
                return
            self.data_rate_profile_setup(port_profile, args, command)

        elif self._validate(args[:3], 'dpbo-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'dpbo-profile', 'quickadd', str)
            name = 'dpbo_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='dpbo')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return

            i = 3
            while i < len(args):
                try:
                    if args[i] == 'working-mode' and re.match("[0-9]+", args[i+1]):
                        port_profile.set('working_mode', int(args[i+1]))
                    elif args[i] == 'eside-electrical-length' and re.match("[0-9]+", args[i+1]) \
                            and re.match("[0-9]+", args[i+2]):
                        length = args[i+1] + ' ' + args[i+2]
                        port_profile.set('eside_electrical_length', length)
                    elif args[i] == 'assumed-exchange-psd' and args[i+1] == 'enable':
                        exchange_psd = args[i+1] + ' ' + args[i+2]
                        port_profile.set('assumed_exchange_psd', exchange_psd)
                    elif args[i] == 'eside-cable-model' and re.match("[0-9]+", args[i+1])\
                            and re.match("[0-9]+", args[i+2]) and re.match("[0-9]+", args[i+3]):
                        model = args[i+1] + ' ' + args[i+2] + ' ' + args[i+3]
                        port_profile.set('eside_cable_model', model)
                    elif args[i] == 'min-usable-signal' and re.match("[0-9]+", args[i+1]):
                        port_profile.set('min_usable_signal', int(args[i+1]))
                    elif args[i] == 'span-frequency' and re.match("[0-9]+", args[i+1]) and re.match("[0-9]+", args[i+2]):
                        freq = args[i+1] + ' ' + args[i+2]
                        port_profile.set('span_frequency', freq)
                    elif args[i] == 'dpbo-calculation' and re.match("[0-9]+", args[i+1]):
                        port_profile.set('dpbo_calculation', int(args[i+1]))
                    elif args[i] == 'desc':
                        port_profile.set('description', args[i + 1])
                except IndexError:
                    raise exceptions.CommandSyntaxError(command=command)

                i += 1

        elif self._validate(args[:3], 'noise-margin-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'noise-margin-profile', 'quickadd', str)
            name = 'noise_margin_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='noise-margin')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return

            i = 3
            while i < len(args):
                try:
                    if args[i] == 'snr-margin' and re.match("[0-9]+", args[i + 1]) and re.match("[0-9]+", args[i + 2]) \
                            and re.match("[0-9]+", args[i + 3]) and re.match("[0-9]+", args[i + 4]) \
                            and re.match("[0-9]+", args[i + 5]) and re.match("[0-9]+", args[i + 6]):
                        margin = args[i+1] + ' ' + args[i+2] + ' ' + args[i+3] + ' ' + args[i+4] + ' ' + args[i+5] + ' ' + \
                                 args[i+6]
                        port_profile.set('snr_margin', margin)
                    elif args[i] == 'rate-adapt' and re.match("[0-9]+", args[i+1]) and re.match("[0-9]+", args[i+2]):
                        adapt = args[i+1] + ' ' + args[i+2]
                        port_profile.set('rate_adapt', adapt)
                    elif args[i] == 'snr-mode':
                        snr_mode = args[i+1] + ' ' + args[i+2]
                        port_profile.set('snr_mode', snr_mode)
                    elif args[i] == 'desc':
                        port_profile.set('description', args[i+1])
                except IndexError:
                    raise exceptions.CommandSyntaxError(command=command)

                i += 1

        elif self._validate(args[:3], 'inp-delay-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'inp-delay-profile', 'quickadd', str)
            name = 'inp_delay_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='inp-delay')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return

            i = 3
            while i < len(args):
                try:
                    if args[i] == ' inp-4.3125khz' and re.match("[0-9]+", args[i+1]) and re.match("[0-9]+", args[i+2]):
                        inp_4 = args[i+1] + ' ' + args[i+2]
                        port_profile.set('inp_4khz', inp_4)
                    elif args[i] == 'inp-8.625khz' and re.match("[0-9]+", args[i+1]) and re.match("[0-9]+", args[i+2]):
                        inp_8 = args[i + 1] + ' ' + args[i + 2]
                        port_profile.set('inp_8khz', inp_8)
                    elif args[i] == 'interleaved-delay' and re.match("[0-9]+", args[i+1]) \
                            and re.match("[0-9]+", args[i+2]):
                        delay = args[i+1] + ' ' + args[i+2]
                        port_profile.set('interleaved_delay', delay)
                    elif args[i] == 'delay-variation' and re.match("[0-9]+", args[i+1]):
                        port_profile.set('delay_variation', int(args[i+1]))
                    elif args[i] == 'channel-policy' and re.match("[0-9]+", args[i+1]):
                        port_profile.set('channel_policy', int(args[i+1]))
                    elif args[i] == 'desc':
                        port_profile.set('description', args[i + 1])
                except IndexError:
                    raise exceptions.CommandSyntaxError(command=command)

                i += 1

        elif self._validate(args[:3], 'mode-specific-psd-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'mode-specific-psd-profile', 'quickadd', str)
            name = 'mode_specific_psd_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='mode-specific-psd')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return
            self.mode_specific_psd_profile_setup(port_profile, args, command)

        elif self._validate(args[:3], 'mode-specific-psd-profile', 'quickmodify', str):
            profile_num, = self._dissect(args[:3], 'mode-specific-psd-profile', 'quickmodify', str)
            name = 'mode_specific_psd_' + profile_num
            try:
                port_profile = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                text = self._render('port_profile_does_not_exist', context=context)
                self._write(text)
                return
            self.mode_specific_psd_profile_setup(port_profile, args, command)

        elif self._validate(args[:3], 'line-spectrum-profile', 'quickadd', str):
            profile_num, = self._dissect(args[:3], 'line-spectrum-profile', 'quickadd', str)
            name = 'line_spectrum_' + profile_num
            try:
                _ = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                self._model.add_port_profile(name=name, type='spectrum')
                try:
                    port_profile = self._model.get_port_profile('name', name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render('port_profile_already_exists', context=context)
                self._write(text)
                return
            self.line_spectrum_profile_setup(port_profile, args, command)

        elif self._validate(args[:3], 'line-spectrum-profile', 'quickmodify', str):
            profile_num, = self._dissect(args[:3], 'line-spectrum-profile', 'quickmodify', str)
            name = 'line_spectrum_' + profile_num
            try:
                port_profile = self._model.get_port_profile('name', name)
            except exceptions.SoftboxenError:
                text = self._render('port_profile_does_not_exist', context=context)
                self._write(text)
                return
            self.line_spectrum_profile_setup(port_profile, args, command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_test(self, command, *args, context=None):

        from .testCommandProcessor import TestCommandProcessor

        if args == ():
            subprocessor = self._create_subprocessor(
                TestCommandProcessor, 'login', 'mainloop', 'enable', 'config', 'test')
            subprocessor.loop(context=context, return_to=ConfigCommandProcessor)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_save(self, command, *args, context=None):
        if args == ():
            # command would save config but other commands do that automatically
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_load(self, command, *args, context=None):  # Read in file
        if self._validate(args, 'script', 'tftp', str, str):
            ip, file_name = self._dissect(args, 'script', 'tftp', str, str)

            try:
                assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip)
                assert ip.count('.') == 3
                for i in ip.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            if not (file_name.endswith('.txt')):
                raise exceptions.CommandSyntaxError(command=command)

            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_sysname(self, command, *args, context=None):
        if args != ():
            name = ''
            for arg in args:
                name += arg
            self._model.set_hostname(name)
            self.set_prompt_end_pos(context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ip(self, command, *args, context=None):
        if self._validate(args, 'route-static', str, str, str):
            dst, sub, gw = self._dissect(args, 'route-static', str, str, str)

            try:
                assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", dst)
                assert dst.count('.') == 3
                for i in dst.split('.'):
                    assert 0 <= int(i) <= 255
                assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", gw)
                assert gw.count('.') == 3
                for i in gw.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            self._model.add_route(dst=dst, gw=gw, sub_mask=sub)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def data_rate_profile_setup(self, port_profile, args, command):
        i = 3
        while i < len(args):
            try:
                if args[i] == 'maximum-bit-error-ratio' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('maximum_bit_error_ratio', int(args[i + 1]))
                elif args[i] == 'path-mode' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('path_mode', int(args[i + 1]))
                elif args[i] == 'rate' and re.match("[0-9]+", args[i + 1]) and re.match("[0-9]+", args[i + 2]) \
                        and re.match("[0-9]+", args[i + 3]) and re.match("[0-9]+", args[i + 4]) \
                        and re.match("[0-9]+", args[i + 5]) and re.match("[0-9]+", args[i + 6]):

                    rate = args[i + 1] + ' ' + args[i + 2] + ' ' + args[i + 3] + ' ' + args[i + 4] + ' ' + args[
                        i + 5] + ' ' + args[i + 6]
                    port_profile.set('rate', rate)
                elif args[i] == 'etr-min' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('etr_min', int(args[i + 1]))
                elif args[i] == 'etr-max' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('etr_max', int(args[i + 1]))
                elif args[i] == 'ndr-max' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('ndr_max', int(args[i + 1]))
                elif args[i] == 'desc':
                    port_profile.set('description', args[i + 1])
            except IndexError:
                raise exceptions.CommandSyntaxError(command=command)

            i += 1
        return

    def mode_specific_psd_profile_setup(self, port_profile, args, command):
        i = 3
        while i < len(args):
            try:
                if args[i] == 'nominal-transmit-PSD-ds' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('nominal_transmit_PSD_ds', int(args[i + 1]))
                elif args[i] == 'nominal-transmit-PSD-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('nominal_transmit_PSD_us', int(args[i + 1]))
                elif args[i] == 'aggregate-transmit-power-ds' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('aggregate_transmit_power_ds', int(args[i + 1]))
                elif args[i] == 'aggregate-transmit-power-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('aggregate_transmit_power_us', int(args[i + 1]))
                elif args[i] == 'aggregate-receive-power-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('aggregate_receive_power_us', int(args[i + 1]))
                elif args[i] == 'upstream-psd-mask-selection' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('upstream_psd_mask_selection', int(args[i + 1]))
                elif args[i] == 'psd-class-mask' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('psd_class_mask', int(args[i + 1]))
                elif args[i] == 'psd-limit-mask' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('psd_limit_mask', int(args[i + 1]))
                elif args[i] == 'desc':
                    port_profile.set('description', args[i + 1])
            except IndexError:
                raise exceptions.CommandSyntaxError(command=command)

            i += 1
        return

    def line_spectrum_profile_setup(self, port_profile, args, command):
        i = 3
        while i < len(args):
            try:
                if args[i] == 'l0-time ' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('l0_time', int(args[i + 1]))
                elif args[i] == 'l2-time' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('l2_time', int(args[i + 1]))
                elif args[i] == 'l3-time' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('l3_time', int(args[i + 1]))
                elif args[i] == 'max-transmite-power-reduction' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('max_transmite_power_reduction', int(args[i + 1]))
                elif args[i] == 'total-max-power-reduction' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('total_max_power_reduction', int(args[i + 1]))
                elif args[i] == 'bit-swap-ds' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('bit_swap_ds', int(args[i + 1]))
                elif args[i] == 'bit-swap-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('bit_swap_us', int(args[i + 1]))
                elif args[i] == 'overhead-datarate-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('overhead_datarate_us', int(args[i + 1]))
                elif args[i] == 'overhead-datarate-ds' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('overhead_datarate_ds', int(args[i + 1]))
                elif args[i] == 'allow-transitions-to-idle' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('allow_transitions_to_idle', int(args[i + 1]))
                elif args[i] == 'allow-transitions-to-lowpower' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('allow_transitions_to_lowpower', int(args[i + 1]))
                elif args[i] == 'reference-clock':
                    port_profile.set('reference_clock', args[i + 1])
                elif args[i] == 'cyclic-extension-flag' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('cyclic_extension_flag', int(args[i + 1]))
                elif args[i] == 'force-inp-ds' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('force_inp_ds', int(args[i + 1]))
                elif args[i] == 'force-inp-us' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('force_inp_us', int(args[i + 1]))
                elif args[i] == 'g.993.2-profile' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('g_993_2_profile', int(args[i + 1]))
                elif args[i] == 'mode-specific' and re.match("[a-z]+", args[i+1]) and re.match("[0-9]+", args[i+2])\
                        and re.match("[0-9]+", args[i+3]):
                    mode = args[i+1] + ' ' + args[i+2] + ' ' + args[i+3]
                    port_profile.set('mode_specific', mode)
                elif args[i] == 'transmode':
                    port_profile.set('transmode', args[i+1])
                elif args[i] == 'T1.413':
                    port_profile.set('T1_413', args[i+1])
                elif args[i] == 'G.992.1':
                    port_profile.set('G_992_1', args[i+1])
                elif args[i] == 'G.992.2':
                    port_profile.set('G_992_2', args[i+1])
                elif args[i] == 'G.992.3':
                    port_profile.set('G_992_3', args[i+1])
                elif args[i] == 'G.992.4':
                    port_profile.set('G_992_4', args[i+1])
                elif args[i] == 'G.992.5':
                    port_profile.set('G_992_5', args[i+1])
                elif args[i] == 'AnnexB' and args[i+1] == 'G.993.2':
                    port_profile.set('AnnexB_G_993_2', args[i+2])
                elif args[i] == 'ETSI':
                    port_profile.set('ETSI', args[i+1])
                elif args[i] == 'us0-psd-mask' and re.match("[0-9]+", args[i + 1]):
                    port_profile.set('us0_psd_mask', int(args[i + 1]))
                elif args[i] == 'vdsltoneblackout':
                    blackout = args[i+1] + ' ' + args[i+2]
                    port_profile.set('vdsltoneblackout', blackout)
                elif args[i] == 'desc':
                    port_profile.set('description', args[i + 1])
            except IndexError:
                raise exceptions.CommandSyntaxError(command=command)
            i += 1
        return
