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
import re
from datetime import datetime, date
from ipaddress import IPv4Network
from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor


class InterfaceCommandProcessor(BaseCommandProcessor):

    def do_return(self, command, *args, context=None):

        from .enableCommandProcessor import EnableCommandProcessor

        exc = exceptions.TerminalExitError()
        exc.return_to = EnableCommandProcessor
        raise exc

    def do_display(self, command, *args, context=None):
        card = context['component']
        if self._validate(args, 'inventory', 'cpe', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            port_identifier, = self._dissect(args, 'inventory', 'cpe', str)
            if card.product == 'vdsl' or card.product == 'adsl':
                try:
                    portname = card.name + "/" + port_identifier
                    port = self._model.get_port("name", portname)
                    cpe = self._model.get_cpe('port_id', port.id)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if not cpe:
                    raise exceptions.CommandSyntaxError(command=command)

                text = self._render(
                    'display_inventory_cpe',
                    context=dict(context, cpe=cpe))
                self._write(text)

        elif self._validate(args, 'vdsl', 'line-profile', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if self._model.dsl_mode == 'tr129':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'vdsl':
                vdsl_id, = self._dissect(args, 'vdsl', 'line-profile', str)
                try:
                    profile = self._model.get_port_profile('name', 'line_spectrum_' + str(vdsl_id))

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                text = self._render('display_vdsl_line-profile_num', context=dict(context, profile=profile))
                self._write(text)
            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'adsl', 'line-profile', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if self._model.dsl_mode == 'tr129':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'adsl':
                adsl_id, = self._dissect(args, 'adsl', 'line-profile', str)
                try:
                    profile = self._model.get_port_profile('name', 'line_spectrum_' + str(adsl_id))
                    txt = ''
                    if profile.G_992_1 == 'enable':
                        txt += 'G_992_1'
                    if profile.G_992_2 == 'enable':
                        txt += ', G_992_2'
                    if profile.G_992_3 == 'enable':
                        txt += ', G_992_3'
                    if profile.G_992_4 == 'enable':
                        txt += ', G_992_4'
                    if profile.G_992_5 == 'enable':
                        txt += ', G_992_5'
                    if profile.T1_413 == 'enable':
                        txt += ', T1.413'
                    if len(txt.split(',')) == 6:
                        context['trmode'] = 'All(G.992.1~5,T1.413)'
                    else:
                        context['trmode'] = txt
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                text = self._render('display_adsl_line-profile_num', context=dict(context, profile=profile))
                self._write(text)
            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'power', 'run', 'info'):
            emu = context['component']
            if context['iftype'] == 'emu' and emu.type == 'H831PMU':
                context['spacer1'] = self.create_spacers((11,), (emu.limit_state,))[0] * ' '
                context['spacer2'] = self.create_spacers((11,), (emu.module_0_address,))[0] * ' '
                context['spacer3'] = self.create_spacers((11,), (emu.module_0_voltage,))[0] * ' '
                context['spacer4'] = self.create_spacers((11,), (emu.dc_voltage,))[0] * ' '
                text = self._render('display_power_run_info', context=dict(context, emu=emu))
                self._write(text)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args, 'port', 'state', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth-pon':
                port_id, = self._dissect(args, 'port', 'state', str)
                portname = card.name + "/" + port_id

                try:
                    port = self._model.get_port("name", portname)
                    self.map_states(port, 'port')

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if port.operational_state == 'activated':
                    text = self._render(
                        'display_port_state',
                        context=dict(context, port=port))
                else:
                    text = self._render(
                        'display_port_state_offline',
                        context=dict(context, port=port))
                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'ont', 'port', 'state', str, str, 'eth-port', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth-pon':
                port_idx, ont_idx, ont_port_idx, = self._dissect(
                    args, 'ont', 'port', 'state', str, str, 'eth-port', str)

                try:
                    portname = card.name + '/' + port_idx
                    port = self._model.get_port('name', portname)
                    ontname = portname + '/' + ont_idx
                    ont = self._model.get_ont('name', ontname)
                    ont_portname = ontname + '/' + ont_port_idx
                    ont_port = self._model.get_ont_port('name', ont_portname)

                except exceptions.SoftboxenError:
                    self._write(self._render('ont_not_online', context=context))
                    return

                if port.id != ont.port_id or ont_port.ont_id != ont.id:
                    raise exceptions.CommandSyntaxError(command=command)

                context['ont_id'] = ont_idx
                context['ont_port_id'] = ont_port_idx

                context['spacer1'] = self.create_spacers((8,), (ont_idx,))[0] * ' '
                context['spacer2'] = self.create_spacers((10,), (ont_port_idx,))[0] * ' '
                context['spacer3'] = self.create_spacers((11,), (ont_port.ont_port_type,))[0] * ' '
                context['spacer4'] = self.create_spacers((1,), ('',))[0] * ' '
                context['spacer5'] = self.create_spacers((14,), (ont_port.speed,))[0] * ' '
                context['spacer6'] = self.create_spacers((9,), (ont_port.duplex,))[0] * ' '
                context['spacer7'] = self.create_spacers((11,), (ont_port.link_state,))[0] * ' '

                text = self._render('display_ont_port_state_num_num_eth-port_num',
                                    context=dict(context, ont_port=ont_port))
                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'ont', 'info', str, str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth-pon':
                port_idx, ont_idx, = self._dissect(
                    args, 'ont', 'info', str, str)

                try:
                    portname = card.name + "/" + port_idx
                    ontname = portname + "/" + ont_idx
                    port = self._model.get_port("name", portname)
                    ont = self._model.get_ont("name", ontname)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                time_now_str = str(datetime.now())[:19] + '+01:00'
                time_now = datetime.strptime(time_now_str, "%Y-%m-%d %H:%M:%S+01:00")
                last_up = datetime.strptime(ont.last_up_time, "%Y-%m-%d %H:%M:%S+01:00")
                online_duration = time_now - last_up
                ont.set_online_duration(str(online_duration))
                ont = self._model.get_ont("name", ontname)
                self.map_states(ont, 'ont')

                context['ont_idx'] = ont.index

                context['spacer1'] = self.create_spacers((16,), (ont.port_number_pots,))[0] * ' '
                context['spacer2'] = self.create_spacers((16,), (ont.port_number_eth,))[0] * ' '
                context['spacer3'] = self.create_spacers((16,), (ont.port_number_vdsl,))[0] * ' '

                text_header = self._render('display_ont_info_port_ont_header',
                                           context=dict(context, port=port, ont=ont))
                text1 = ''
                text2 = ''
                text3 = ''
                text4 = self._render('display_ont_info_port_ont_loop4_top', context=context)
                text_vlan = self._render('display_ont_info_port_ont_vlan_top', context=context)

                check_if_vlan = False

                ont_ports = self._model.get_ont_ports('ont_id', ont.id)

                for ont_port in ont_ports:
                    context['spacer4'] = self.create_spacers((2,), ('',))[0] * ' '
                    context['spacer5'] = self.create_spacers((10,), (ont_port.ont_port_type,))[0] * ' '
                    context['spacer6'] = self.create_spacers((8,), (ont_port.ont_port_index,))[0] * ' '
                    context['spacer7'] = self.create_spacers((10,), (ont_port.qinq_mode,))[0] * ' '
                    context['spacer8'] = self.create_spacers((15,), (ont_port.priority_policy,))[0] * ' '
                    context['spacer9'] = self.create_spacers((12,), (ont_port.inbound,))[0] * ' '
                    text1 += self._render('display_ont_info_port_ont_loop1_middle',
                                          context=dict(context, ont_port=ont_port))

                    context['spacer10'] = self.create_spacers((2,), ('',))[0] * ' '
                    context['spacer11'] = self.create_spacers((16,), (ont_port.ont_port_type,))[0] * ' '
                    context['spacer12'] = self.create_spacers((2,), ('',))[0] * ' '
                    context['spacer13'] = self.create_spacers((16,), (ont_port.downstream_mode,))[0] * ' '
                    text2 += self._render('display_ont_info_port_ont_loop2_middle',
                                          context=dict(context, ont_port=ont_port))

                    context['spacer14'] = self.create_spacers((2,), ('',))[0] * ' '
                    context['spacer15'] = self.create_spacers((10,), (ont_port.ont_port_type,))[0] * ' '
                    context['spacer16'] = self.create_spacers((8,), (ont_port.ont_port_index,))[0] * ' '
                    text3 += self._render('display_ont_info_port_ont_loop3_middle',
                                          context=dict(context, ont_port=ont_port))

                    context['spacer17'] = self.create_spacers(
                        (18,), (ont_port.ont_port_type + str(ont_port.ont_port_index),))[0] * ' '
                    context['spacer18'] = self.create_spacers((4,), ('',))[0] * ' '
                    context['spacer19'] = self.create_spacers((27,),
                                                              (ont_port.igmp_mode + ont_port.igmp_vlan,))[0] * ' '
                    context['spacer20'] = self.create_spacers((10,), (ont_port.igmp_pri,))[0] * ' '
                    context['spacer21'] = self.create_spacers((15,), (ont_port.max_mac_count,))[0] * ' '
                    text4 += self._render('display_ont_info_port_ont_loop4_middle',
                                          context=dict(context, ont_port=ont_port))

                    if ont_port.vlan_id is not None:
                        check_if_vlan = True
                        context['spacer22'] = self.create_spacers((7,), (ont_port.ont_port_type,))[0] * ' '
                        context['spacer23'] = self.create_spacers((7,), (ont_port.ont_port_index,))[0] * ' '
                        context['spacer24'] = self.create_spacers((13,), (ont_port.service_type,))[0] * ' '
                        context['spacer25'] = self.create_spacers((6,), (ont_port.service_index,))[0] * ' '
                        context['spacer26'] = self.create_spacers((7,), (ont_port.s_vlan,))[0] * ' '
                        context['spacer27'] = self.create_spacers((6,), (ont_port.s_pri,))[0] * ' '
                        context['spacer28'] = self.create_spacers((7,), (ont_port.c_vlan,))[0] * ' '
                        context['spacer29'] = self.create_spacers((6,), (ont_port.c_pri,))[0] * ' '
                        context['spacer30'] = self.create_spacers((11,), (ont_port.encap,))[0] * ' '
                        text_vlan += self._render('display_ont_info_port_ont_vlan_middle',
                                                  context=dict(context, ont_port=ont_port))

                text1 += self._render('display_ont_info_port_ont_loop1_loop2', context=context)
                text2 += self._render('display_ont_info_port_ont_loop2_loop3', context=context)
                text4 += self._render('display_ont_info_port_ont_loop4_bottom', context=context)
                text_vlan += self._render('display_ont_info_port_ont_vlan_bottom', context=context)

                if check_if_vlan:
                    text = text_header + text1 + text2 + text3 + text_vlan + text4
                else:
                    text = text_header + text1 + text2 + text3 + text4

                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'ont', 'optical-info', str, str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth-pon':
                port_idx, ont_idx, = self._dissect(
                    args, 'ont', 'optical-info', str, str)

                try:
                    portname = card.name + "/" + port_idx
                    ontname = portname + "/" + ont_idx
                    _ = self._model.get_port("name", portname)
                    _ = self._model.get_ont("name", ontname)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                text = self._render('display_ont_optical-info_num_num', context=context)
                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'port', 'ddm-info', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth':
                port_idx, = self._dissect(args, 'port', 'ddm-info', str)

                try:
                    portname = card.name + "/" + port_idx
                    port = self._model.get_port('name', portname)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if self._model.smart_mode:
                    self.user_input('{ <cr>|sort-by<K>||<K> }:')
                text = self._render(
                    'display_port_ddm-info',
                    context=dict(context, port=port))
                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'traffic', 'table', 'ip', 'index', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'ftth-pon':
                ip_index, = self._dissect(args, 'traffic', 'table', 'ip', 'index', str)
                context['ip_index'] = ip_index
                context['cir'] = random.randint(0, 10000)
                context['cbs'] = random.randint(1000, 100000)
                context['pir'] = random.randint(0, 10000)
                context['pbs'] = random.randint(1000, 100000)

                text = self._render('display_traffic_table_ip_index', context=context)
                self._write(text)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_activate(self, command, *args, context=None):
        card = context['component']
        if self._validate(args[:6], str, 'prof-desc', 'ds-rate', str, 'us-rate', str):
            spectrum_flag = False
            dpbo_flag = False
        #elif self._validate(args, str, 'prof.desc', 'ds-rate', str, 'us-rate', str, '(spectrum str)', 'noise-margin', 'ADSL_6db', 'inp-delay', 'ADSL','(dpbo DPBO:str)'):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if self._model.dsl_mode == 'tr129':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'vdsl':
                port_idx, ds_rate, us_rate = self._dissect(args[:6], str, 'prof-desc', 'ds-rate', str, 'us-rate', str)

                try:
                    port_name = card.name + '/' + port_idx
                    port = self._model.get_port("name", port_name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                i = 6
                while i < len(args):
                    if args[i] == 'spectrum':
                        spectrum = args[i+1]
                        i += 2
                        try:
                            profile = self._model.get_port_profile('description', spectrum)
                            spectrum_profile = 'No. ' + str(profile.number) + ' ' + spectrum
                            spectrum_id = str(profile.number)
                        except exceptions.SoftboxenError:
                            raise exceptions.CommandSyntaxError(command=command)
                        else:
                            spectrum_flag = True
                    elif args[i] == 'noise-margin':
                        noise = args[i+1]
                        i += 2
                        try:
                            profile = self._model.get_port_profile('description', noise)
                            noise_profile = 'No. ' + str(profile.number) + ' ' + noise
                            noise_id = str(profile.number)
                        except exceptions.SoftboxenError:
                            raise exceptions.CommandSyntaxError(command=command)
                    elif args[i] == 'inp-delay':
                        inp = args[i+1]
                        i += 2
                        try:
                            profile = self._model.get_port_profile('description', inp)
                            inp_profile = 'No. ' + str(profile.number) + ' ' + inp
                            inp_id = str(profile.number)
                        except exceptions.SoftboxenError:
                            raise exceptions.CommandSyntaxError(command=command)
                    elif args[i] == 'dpbo':
                        dpbo = args[i+1]
                        i += 2
                        try:
                            profile = self._model.get_port_profile('description', dpbo)
                            dpbo_profile = 'No. ' + str(profile.number) + ' ' + dpbo
                            dpbo_id = str(profile.number)
                        except exceptions.SoftboxenError:
                            raise exceptions.CommandSyntaxError(command=command)
                        else:
                            dpbo_flag = True
                    else:
                        raise exceptions.CommandSyntaxError(command=command)

                try:
                    port.admin_up()
                    port.set('downstream_max', ds_rate)
                    port.set('upstream_max', us_rate)
                    if spectrum_flag:
                        port.set('line_spectrum_profile', spectrum_profile)
                        port.set('spectrum_profile_num', spectrum_id)
                    port.set('noise_margin_profile', noise_profile)
                    port.set('noise_margin_profile_num', noise_id)
                    port.set('inm_profile', inp_profile)
                    port.set('inm_profile_num', inp_id)
                    if dpbo_flag:
                        port.set('dpbo_profile', dpbo_profile)
                        port.set('dpbo_profile_num', dpbo_id)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, str, 'template-name', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if self._model.dsl_mode == 'tr165':
                raise exceptions.CommandSyntaxError(command=command)
            if card.product == 'adsl' or card.product == 'vdsl':
                # Template looks like this: {huawei_downstream}_{huawei_downstream}_ADSL
                # Template looks like this: {huawei_downstream}_{huawei_downstream}_{summary} vdsl
                port_idx, template_name = self._dissect(args, str, 'template-name', str)

                try:
                    port_name = card.name + '/' + port_idx
                    port = self._model.get_port("name", port_name)
                    port.admin_up()
                    port.set_template_name(template_name)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args, 'all'):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if context['iftype'] not in ('adsl', 'vdsl'):
                self._write(self._render('operation_not_supported_by_port_failure', context=context))
                return
            self.card_ports_up(card)
        elif self._validate(args, str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if context['iftype'] not in ('adsl', 'vdsl'):
                self._write(self._render('operation_not_supported_by_port_failure', context=context))
                return
            port_identifier, = self._dissect(
                args, str)

            try:
                portname = card.name + '/' + port_identifier
                port = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if port.admin_state == '2':
                self._write(self._render('port_has_been_activated', context=dict(context, port_name=port.name.split('/')[2])))
                return

            port.admin_up()

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_deactivate(self, command, *args, context=None):
        if context['iftype'] == 'vlanif':
            raise exceptions.CommandSyntaxError(command=command)
        if context['iftype'] not in ('adsl', 'vdsl'):
            raise exceptions.CommandSyntaxError(command=command)
        card = context['component']
        if self._validate(args, 'all'):
            self.card_ports_down(card)
        elif self._validate(args, str):
            port_identifier, = self._dissect(args, str)
            try:
                portname = card.name + '/' + port_identifier
                port = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if port.admin_state == '0':
                self._write(self._render('port_has_been_deactivated', context=dict(context, port_name=port.name.split('/')[2])))
                return

            port.admin_down()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        component = context['component']
        if self._validate(command, '?'):
            if hasattr(component, 'product'):
                if component.product == 'vdsl':
                    text = self._render(
                        'vdsl_help',
                        context=context)
                    self._write(text)
                elif component.product == 'ftth-pon':
                    text = self._render(
                        'gpon_help',
                        context=context)
                    self._write(text)
                elif component.product == 'adsl':
                    text = self._render(
                        'adsl_help',
                        context=context)
                    self._write(text)
                else:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                text = self._render(
                    'vlan_help',
                    context=context)
                self._write(text)
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vectoring_config(self, command, *args, context=None):
        card = context['component']
        if self._validate(args, str, 'profile-index', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            port_identifier, profile_idx = self._dissect(args, str, 'profile-index', str)
            try:
                portname = card.name + '/' + port_identifier
                port = self._model.get_port("name", portname)
                self._model.get_port_profile('id', int(profile_idx))
                port.set_vectoring_profile_id(int(profile_idx))

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shutdown(self, command, *args, context=None):
        if context['iftype'] == 'vlanif':
            raise exceptions.CommandSyntaxError(command=command)
        if context['iftype'] not in ('opg', 'eth'):
            self._write(self._render('operation_not_supported_by_port_failure', context=context))
            return
        card = context['component']
        if self._validate(args, 'all'):
            self.card_ports_down(card)
        elif self._validate(args, str):
            port_identifier, = self._dissect(args, str)
            try:
                portname = card.name + '/' + port_identifier
                port = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            port.admin_down()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ont(self, command, *args, context=None):
        if self._validate(args[:11], 'add', str, str, 'sn-auth', str, 'omci', 'ont-lineprofile-id', str, 'ont-srvprofile-id',
                          str, 'desc'):
            port_idx, ont_idx, cpe_device_id, lineprofile_id, srvprofile_id = \
                self._dissect(args[:11], 'add', str, str, 'sn-auth', str, 'omci', 'ont-lineprofile-id', str,
                              'ont-srvprofile-id', str, 'desc')

            def arg_joiner(arguments):
                saved_args = []
                save = False

                if len(arguments) == 1:
                    return arguments

                for i in range(len(arguments)):
                    if arguments[i].startswith("\""):
                        save = True
                    if save:
                        saved_args.append(arguments[i])
                    if arguments[i].endswith("\""):
                        save = False
                arg = ' '.join(saved_args).replace("\"", "")

                return arg

            description = arg_joiner(args[11:])

            card = context['component']
            port = self._model.get_port('name', card.name + '/' + port_idx)

            ont = None
            try:
                ont = self._model.get_ont('name', card.name + '/' + port_idx + '/' + ont_idx)
            except exceptions.InvalidInputError:
                pass

            if ont is not None:
                self._write(self._render('ont_already_exists', context=context))
                return

            self._model.add_ont(port_id=port.id, name=card.name + '/' + port_idx + '/' + ont_idx,
                                      description=description, lineprofile_id=lineprofile_id,
                                      srvprofile_id=srvprofile_id)

            self._write(self._render('ont_added', context=context))
        elif self._validate(args, 'delete', str, str):
            # delete all subcomponents
            port_idx, ont_idx = self._dissect(args, 'delete', str, str)
            card = context['component']
            try:
                ont = self._model.get_ont('name', card.name + '/' + port_idx + '/' + ont_idx)
                ont_ports = self._model.get_ont_ports('ont_id', ont.id)
                if len(ont_ports) != 0:
                    cpes = []
                    for ont_port in ont_ports:
                        cpes.append(self._model.get_cpes('ont_port_id', ont_port.id))
                    if len(cpes) != 0:
                        cpe_ports = []
                        for cpe_coll in cpes:
                            for cpe in cpe_coll:
                                cpe_ports.append(self._model.get_cpe_ports('cpe_id', cpe.id))
                        if len(cpe_ports) != 0:
                            for cpe_port_coll in cpe_ports:
                                for cpe_port in cpe_port_coll:
                                    while True:
                                        params = dict(connected_type='cpe', connected_id=cpe_port.id)
                                        service_port = self._model.get_service_port_by_values(params)
                                        if service_port is None:
                                            break
                                        try:
                                            service_vlan = self._model.get_service_vlan('service_port_id',
                                                                                        service_port.id)
                                        except exceptions.SoftboxenError:
                                            pass
                                        else:
                                            service_vlan.delete()
                                        service_port.delete()
                                    cpe_port.delete()
                        for cpe_coll in cpes:
                            for cpe in cpe_coll:
                                cpe.delete()
                    for ont_port in ont_ports:
                        while True:
                            params = dict(connected_type='ont', connected_id=ont_port.id)
                            service_port = self._model.get_service_port_by_values(params)
                            if service_port is None:
                                break
                            else:
                                try:
                                    service_vlan = self._model.get_service_vlan('service_port_id', service_port.id)
                                except exceptions.SoftboxenError:
                                    pass
                                else:
                                    service_vlan.delete()
                                service_port.delete()
                        ont_port.delete()
                ont.delete()
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'port', 'attribute', str, str, 'eth', str, 'operational-state', str):
            port_idx, ont_idx, ont_port_idx, state = self._dissect(args, 'port', 'attribute', str, str, 'eth', str,
                                                                   'operational-state', str)
            card = context['component']
            try:
                port_name = card.name + '/' + port_idx
                port = self._model.get_port('name', port_name)
                ont_name = port_name + '/' + ont_idx
                ont = self._model.get_ont('name', ont_name)
                ont_port_name = ont_name + '/' + ont_port_idx
                ont_port = self._model.get_ont_port('name', ont_port_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if (ont.port_id != port.id) or (ont_port.ont_id != ont.id):
                raise exceptions.CommandSyntaxError(command=command)

            if state == 'on':
                ont_port.up()
            elif state == 'off':
                ont_port.down()
            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_port(self, command, *args, context=None):
        if context['iftype'] == 'vlanif':
            raise exceptions.CommandSyntaxError(command=command)
        card = context['component']
        if card.product != 'ftth-pon':
            self._write(self._render('operation_not_supported_by_port_failure', context=context))
            return
        if self._validate(args, str, 'ont-auto-find', str):
            port_identifier, mode = self._dissect(args, str, 'ont-auto-find', str)

            port = self._model.get_port('name', card.name + "/" + port_identifier)

            if mode == 'enable':
                port.enable_ont_autofind()
            elif mode == 'disable':
                port.disable_ont_autofind()
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ip(self, command, *args, context=None):
        if self._validate(args, 'address', str, str):
            ip, subnet_mask = self._dissect(args, 'address', str, str)
            if context['iftype'] == 'vlanif':
                vlan_if = context['component']
                try:
                    assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip)
                    assert ip.count('.') == 3
                    for i in ip.split('.'):
                        assert 0 <= int(i) <= 255

                    assert re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", subnet_mask)
                    assert subnet_mask.count('.') == 3
                    for i in subnet_mask.split('.'):
                        assert 0 <= int(i) <= 255
                except (AssertionError, ValueError):
                    raise exceptions.CommandSyntaxError(command=command)

                sub_value = IPv4Network('0.0.0.0/' + subnet_mask).prefixlen
                vlan_if.set('internet_address', ip)
                vlan_if.set('subnet_num', str(sub_value))
                vlan_if.set('internet_protocol', 'enabled')
                box = self._model
                box.set_network_address(ip)
            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_smart(self, command, *args, context=None):
        if self._validate(args,):
            self._write("  Interactive function is enabled\n")
            self._model.enable_smart()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_interactive(self, command, *args, context=None):
        if self._validate(args,):
            self._write("  Interactive function is enabled\n")
            self._model.enable_interactive()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_undo(self, command, *args, context=None):
        if self._validate(args, 'ip', 'address', str, str):
            if context['iftype'] == 'vlanif':
                ip, sub = self._dissect(args, 'ip', 'address', str, str)
                vlan_if = context['component']

                if ip != vlan_if.internet_address or sub != vlan_if.subnet_num:
                    raise exceptions.CommandSyntaxError(command=command)

                vlan_if.set('internet_protocol', 'disabled')
                vlan_if.set('internet_address', None)
                vlan_if.set('subnet_num', None)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args, 'shutdown', 'all'):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if context['iftype'] not in ('opg', 'eth'):
                raise exceptions.CommandSyntaxError(command=command)
            card = context['component']
            self.card_ports_up(card)
        elif self._validate(args, 'shutdown', str):
            if context['iftype'] == 'vlanif':
                raise exceptions.CommandSyntaxError(command=command)
            if context['iftype'] not in ('opg', 'eth'):
                raise exceptions.CommandSyntaxError(command=command)
            port_identifier, = self._dissect(args, 'shutdown', str)
            card = context['component']

            try:
                portname = card.name + '/' + port_identifier
                port = self._model.get_port("name", portname)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            port.admin_up()
        elif self._validate(args, 'smart'):
            self._write("  Interactive function is disabled\n")
            self._model.disable_smart()
        elif self._validate(args, 'interactive'):
            self._write("  Interactive function is disabled\n")
            self._model.disable_interactive()
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def card_ports_down(self, card):
        ports = self._model.get_ports('card_id', card.id)
        if not ports:
            raise exceptions.CommandSyntaxError()
        for port in ports:
            if port.admin_state == '0':
                self._write(self._render('port_has_been_deactivated', context=dict(port_name=port.name.split('/')[2])))
                continue
            port.admin_down()

    def card_ports_up(self, card):
        ports = self._model.get_ports('card_id', card.id)
        if not ports:
            raise exceptions.CommandSyntaxError()
        for port in ports:
            if port.admin_state == '2':
                self._write(self._render('port_has_been_activated', context=dict(port_name=port.name.split('/')[2])))
                continue
            port.admin_up()
