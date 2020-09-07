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


# TODO: Functionality of most functions


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
                    component = self._model.get_vlan_interface("name", vlan_if_name)
                    check = True

                except exceptions.SoftboxenError:
                    text = self._render('vlan_does_not_exist', context=context)
                    self._write(text)
                    return

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
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_display(self, command, *args, context=None):
        if self._validate(args, 'board', str):
            self.display_board(command, args, context)
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
                    context['ont_count'] += 1
                    if ont.run_state == 'online':
                        context['ont_online_count'] += 1
                    context['ont_idx'] = ont.name.split("/")[-1]
                    context['ont_serial_number'] = ont.serial_number
                    context['ont_description'] = ont.description
                    context['ont_distance'] = random.randint(distance, distance + 1000)
                    context['rx_power'] = round(random.uniform(15, 25), 2)
                    context['tx_power'] = round(random.uniform(1, 3), 2)
                    context['ont_run_state'] = ont.run_state
                    date = datetime.date.today() - datetime.timedelta(days=random.randint(7, 28))
                    if ont.run_state == 'online':
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
            text = ''
            if len(components) == 1:
                try:
                    subrack = self._model.get_subrack('name', identifier)
                except exceptions.InvalidInputError:
                    self.on_error(context=context)
                    return
                cards = self._model.get_cards('subrack_id', subrack.id)
                for card in cards:
                    if card.product != 'ftth-pon':
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
                if card.product != 'ftth-pon':
                    self.on_error(context=context)
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
                if card.product != 'ftth-pon':
                    self.on_error(context=context)
                text += generate_ont_info_summary(port)
            else:
                raise exceptions.CommandSyntaxError

            self._write(text)
        elif self._validate(args, 'interface', 'vlanif', str):
            vlan_number, = self._dissect(args, 'interface', 'vlanif', str)
            try:
                vlan = self._model.get_vlan("number", int(vlan_number))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('display_interface_vlanif_num', context=dict(context, vlan=vlan))
            self._write(text)
        elif self._validate(args, 'vlan', 'all'):
            _ = self.user_input('{ <cr>|vlanattr<K>|vlantype<E><mux,standard,smart> }:')
            text = self._render('display_vlan_all_top', context=context)
            count = 0
            for vlan in self._model.vlans:  # TODO: STND_Port_NUM + SERV_Port_NUM hinzufügen + Service_Vlans?
                context['spacer1'] = self.create_spacers((6,), (vlan.number,))[0] * ' '
                context['spacer2'] = self.create_spacers((10,), (vlan.type,))[0] * ' '
                context['spacer3'] = self.create_spacers((23,), (vlan.attribute,))[0] * ' '
                text += self._render('display_vlan_all_mid', context=dict(context, vlan=vlan))
                count += 1

            text += self._render('display_vlan_all_bottom', context=dict(context, count=count))
            self._write(text)

        elif self._validate(args, 'vdsl', 'line-profile', str):  # TODO: Check if line-profile exists
            vdsl_id, = self._dissect(args, 'vdsl', 'line-profile', str)
            context['vdsl_id'] = vdsl_id
            text = self._render('display_vdsl_line-profile_num', context=context)
            self._write(text)

        elif self._validate(args, 'adsl', 'line-profile', str):  # TODO: Check if line-profile exists
            adsl_id, = self._dissect(args, 'adsl', 'line-profile', str)
            context['adsl_id'] = adsl_id
            text = self._render('display_adsl_line-profile_num', context=context)
            self._write(text)

        elif self._validate(args, 'version'):
            self.user_input('{ <cr>|backplane<K>|frameid/slotid<S><Length 1-15> }:')
            text = self._render('display_version', context=dict(context, box=self._model))
            self._write(text)

        elif self._validate(args, 'alarm', 'active', 'alarmtype', 'environment', 'detail'):
            text = self._render(
                'display_alarm_active_alarmtype_environment_detail',
                context=context)
            self._write(text)

        elif self._validate(args, 'pitp', 'config'):
            text = self._render(
                'display_pitp_config',
                context=context)
            self._write(text)

        elif self._validate(args, 'mac-address', 'all'):
            self.user_input('{ <cr>||<K> }:')
            text = self._render(
                'display_mac-address_all',
                context=context)
            self._write(text)

        elif self._validate(args, 'current-configuration', 'section', 'vlan-srvprof'):
            self.user_input('{ <cr>||<K> }:')
            text = self._render('display_current_configuration_section_vlan_srvprof_top', context=dict(context, box=self._model))
            text2 = ''
            for vlan in self._model.vlans:
                try:
                    if vlan.bind_service_profile_id != '-' and int(vlan.bind_service_profile_id) >= 0:
                        profile = self._model.get_port_profile("id", int(vlan.bind_service_profile_id))
                        text += self._render('display_current_configuration_section_vlan_srvprof_mid',
                                             context=dict(context, vlan=vlan, profile=profile))
                        text2 += self._render('display_current_configuration_section_vlan_srvprof_bot',
                                              context=dict(context, vlan=vlan, profile=profile))

                except ValueError:
                    raise exceptions.CommandSyntaxError(command=command)
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
            addr,  = self._dissect(args, 'unicast-server', str)
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

    def do_time(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'dst', 'start', '3', 'last', 'Sun', '02:00:00', 'end', '10', 'last', 'Sun', '03:00:00',
                          'adjust', '01:00'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vlan(self, command, *args, context=None):
        if self._validate(args, 'bind', 'service-profile', str, 'profile-id', str):
            trafficvlan, id = self._dissect(args, 'bind', 'service-profile', str, 'profile-id', str)
            try:
                vlan = self._model.get_vlan("number", int(trafficvlan))
                profile = self._model.get_port_profile("id", int(id))
                assert profile.box_id == self._model.id
                assert profile.type == "service"
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            vlan.set_service_profile_id(int(id))
            text = self._render(
                'vlan_bind_service-profile_vlan-id_profile-id_profile-id',
                context=context)
            self._write(text)

        elif self._validate(args, 'service-profile', 'profile-name', str, 'profile-id', str):  # TODO: Functionality
            name, id = self._dissect(args, 'service-profile', 'profile-name', str, 'profile-id', str)
            return

        elif self._validate(args, str, 'smart'):
            trafficvlan,  = self._dissect(args, str, 'smart')
            try:
                vlan = self._model.get_vlan("number", int(trafficvlan))
            except exceptions.SoftboxenError:
                self._model.add_vlan(number=int(trafficvlan), name='VLAN_'+trafficvlan)
                try:
                    vlan = self._model.get_vlan("number", int(trafficvlan))
                    interface_name = 'vlanif' + trafficvlan
                    self._model.add_vlan_interface(name=interface_name, vlan_id=vlan.id)
                    vlan_interface = self._model.get_vlan_interface('name', interface_name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                return

            text = self._render('vlan_already_exists', context=context)
            self._write(text)
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio_format(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'pitp-pmode', 'cid', 'eth', '"anid', 'eth', 'slot/port+1"'):
            return

        elif self._validate(args, 'pitp-pmode', 'cid', 'atm', '"anid', 'atm', 'slot/port+1:vpi:vci"'):
            return

        elif self._validate(args, 'pitp-pmode', 'rid', 'plabel'):
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio(self, command, *args, context=None):  # TODO: Functionality
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

    def do_pitp(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'enable', 'pmode'):
            text = self._render(
                'pitp_enable_pmode',
                context=context)
            self._write(text)

        elif self._validate(args, 'enable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'disable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_raio_mode(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'user-defined', 'pitp-pmode'):
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

    def do_forwarding(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'vlan-mac'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_packet_policy(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'multicast', 'forward'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'unicast', 'discard'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_security(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'anti-macspoofing', 'disable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'anti-macspoofing', 'enable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'anti-ipspoofing', 'disable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'anti-ipspoofing', 'enable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vmac(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'disable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        elif self._validate(args, 'enable'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_igmp(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'mismatch', 'transparent'):
            text = self._render(
                'please_wait_commit',
                context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_commit(self, command, *args, context=None):  # TODO: Functionality
        return

    def do_undo(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'system', 'snmp-user', 'password', 'security'):
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
            return
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

            text = self._render('delete_vlan_if_first', context=context)    # TODO: create template
            self._write(text)
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_snmp_agent(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'community', 'read', '%S0O&R^7OW*+Xa9W4YQ.U=1!!B#A8&)VAB\']]F;U$19\'2_1!!%"'):
            return
        elif self._validate(args, 'community', 'write', '%0;OY:ZN9E3#]`FQ^XRO$#A!!B#A8&)VAB\']]F;U$19\'2_1!!%"'):
            return
        elif self._validate(args, 'target-host', 'trap-hostname', 'test_U2000', 'address', str,
                            'udp-port', '162', 'trap-paramsname', 'test_U2000"'):
            return
        elif self._validate(args, 'target-host', 'trap-paramsname', 'test_U2000', 'v1', 'securityname',
                            '%S0O&R^7OW*+Xa9W4YQ.U=1!!B#A8&)VAB\']]F;U$19\'2_1!!%"'):
            return
        elif self._validate(args, 'trap', 'enable', 'standard'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_system(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'handshake', 'interval', '300'):
            return
        elif self._validate(args, 'handshake', 'enable'):
            return
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
                return
            while len(login) < 6:
                text = self._render('terminal_name_short', context=context)
                self._write(text)
                login = self.user_input("  User Name(length<6,15>):", False, 15)

            password = self.user_input("  User Password(length<6,15>):", False, )
            while len(password) < 6:
                text = self._render('terminal_pw_short', context=context)
                self._write(text)
                password = self.user_input("  User Password(length<6,15>):", False, 15)

            password_repeat = self.user_input("  Confirm Password(length<6,15>):", False)
            while password != password_repeat:
                text = self._render('terminal_pw_error', context=context)
                self._write(text)
                password_repeat = self.user_input("  Confirm Password(length<6,15>):", False, 15)

            profile = self.user_input("  User profile name(<=15 chars)[root]:", False)
            while (profile != 'root') and (profile != 'admin') and (profile != 'operator') and (profile != 'commonuser'):
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

            var_n = self.user_input("  Repeat this operation? (y/n)[n]:", False)
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
                port = self._model.get_port("name", portident)
                vlan = self._model.get_vlan("number", int(trafficvlan))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            try:            # Check if s_port exists
                service_port = self._model.get_service_port("name", portident)
            except exceptions.SoftboxenError:
                self._model.add_service_port(name=portident, connected_id=port.id, connected_type='port',
                                             bytes_us=port.total_bytes_us, packets_us=port.total_packets_us,
                                             bytes_ds=port.total_bytes_ds, packets_ds=port.total_packets_ds)
                try:
                    service_port = self._model.get_service_port("name", portident)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            params = dict(name=str(vlan.number), service_port_id=service_port.id)
            service_vlan = self._model.get_service_vlan_by_values(params)
            if service_vlan is None:
                self._model.add_service_vlan(name=vlan.number, vlan_id=vlan.id, service_port_id=service_port.id)
                try:
                    service_vlan = self._model.get_service_vlan_by_values(params)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_deactivate(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'all'):
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_xdsl(self, command, *args, context=None):  # TODO: Functionality
        if self._validate(args, 'vectoring-group', 'link', 'add', str, str):
            profile_idx, port_idx = self._dissect(args, 'vectoring-group', 'link', 'add', str, str)
            portname = port_idx[0:3] + '/' + port_idx[4]

            try:
                _ = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            return

        elif self._validate(args, 'vectoring-group', 'link', 'delete', str, str):
            profile_idx, port_idx = self._dissect(args, 'vectoring-group', 'link', 'delete', str, str)
            portname = port_idx[0:3] + '/' + port_idx[4]

            try:
                _ = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            return

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
            # Saves the config that was entered
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_load(self, command, *args, context=None):  # TODO: Read in file
        if self._validate(args, 'script', 'tftp', str, str):
            ip, file_name = self._dissect(args, 'script', 'tftp', str, str)

            try:
                assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip)
                assert ip.count('.') == 3
                for i in ip.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            if not(file_name.endswith('.txt')):
                raise exceptions.CommandSyntaxError(command=command)

            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_sysname(self, command, *args, context=None):  # TODO: Functionality
        if args != ():
            name = ''
            for arg in args:
                name += arg
            self._model.change_hostname(name)
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
