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

from vendors.Huawei.baseCommandProcessor import BaseCommandProcessor
from nesi import exceptions


class HuaweiBaseCommandProcessor(BaseCommandProcessor):

    def display_board(self, command, args, context=None):
        identifier, = self._dissect(args, 'board', str)
        if identifier == '0':
            text = self._render('display_board_0_top', context=context)

            sorted_cards = []
            for card in self._model.cards:
                card_id = int(card.name[2:])
                sorted_cards.append(card_id)

            sorted_cards = sorted(sorted_cards)

            for i in range(0, sorted_cards[-1]+1):
                if i not in sorted_cards:
                    context['cardname'] = i
                    text += self._render('display_board_0_empty', context=context)

                else:
                    try:
                        cardname = '0/' + str(i)
                        card = self._model.get_card('name', cardname)
                    except exceptions.SoftboxenError:
                        raise exceptions.CommandSyntaxError(command=command)
                    context['cardname'] = i

                    context['spacer1'] = self.create_spacers((8,), (cardname,))[0] * ' '
                    context['spacer2'] = self.create_spacers((11,), (card.board_name,))[0] * ' '
                    context['spacer3'] = self.create_spacers((17,), (card.board_status,))[0] * ' '
                    context['spacer4'] = self.create_spacers((9,), (card.sub_type_0,))[0] * ' '
                    context['spacer5'] = self.create_spacers((12,), (card.sub_type_1,))[0] * ' '

                    text += self._render('display_board_0_middle', context=dict(context, card=card))

            text += self._render('display_board_0_bottom', context=context)
            self._write(text)

        else:
            try:
                card = self._model.get_card("name", identifier)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product == 'vdsl' or card.product == 'adsl':
                text1 = ''
                text2 = ''
                text3 = ''

                text1 += self._render('display_board_dsl_product_top_top', context=dict(context, card=card))
                text2 += self._render('display_board_dsl_product_middle_top', context=context)
                text3 += self._render('display_board_dsl_product_bottom_top', context=context)

                ports = self._model.get_ports('card_id', card.id)

                activated_count = 0
                port_counter = 0

                for port in ports:
                    self.map_states(port, 'port')
                    if port.admin_state == 'activated':
                        activated_count += 1
                    _, _, portname = port.name.split('/')
                    context['portname'] = portname
                    if card.product == 'vdsl':
                        porttype = 'VDSL'
                    else:
                        porttype = 'ADSL'
                    context['porttype'] = porttype
                    context['spacer_beg1'] = self.create_spacers((6,), (portname,))[0] * ' '
                    context['spacer1'] = self.create_spacers((7,), (porttype,))[0] * ' '
                    context['spacer2'] = self.create_spacers((3,), ('',))[0] * ' '
                    context['spacer3'] = self.create_spacers(
                        (25,), (port.admin_state + str(port.alarm_template_num),))[0] * ' '
                    context['spacer4'] = self.create_spacers((13,), (port.spectrum_profile_num,))[0] * ' '
                    context['spacer5'] = self.create_spacers((13,), (port.upbo_profile_num,))[0] * ' '
                    text1 += self._render('display_board_dsl_product_top_middle',
                                          context=dict(context, port=port))
                    port_counter += 1

                    context['spacer_beg2'] = self.create_spacers((6,), (portname,))[0] * ' '
                    context['spacer6'] = self.create_spacers((11,), (port.sos_profile_num,))[0] * ' '
                    context['spacer7'] = self.create_spacers((11,), (port.dpbo_profile_num,))[0] * ' '
                    context['spacer8'] = self.create_spacers((13,), (port.rfi_profile_num,))[0] * ' '
                    context['spacer9'] = self.create_spacers((13,), (port.noise_margin_profile_num,))[0] * ' '
                    context['spacer10'] = self.create_spacers((13,), (port.virtual_noise_profile_num,))[0] * ' '
                    context['spacer11'] = self.create_spacers((13,), (port.inm_profile_num,))[0] * ' '
                    text2 += self._render('display_board_dsl_product_middle_middle', context=dict(context,
                                                                                                  port=port))

                    channelname = portname + '.1'
                    context['channelname'] = channelname
                    context['spacer_beg3'] = self.create_spacers((7,), (channelname,))[0] * ' '
                    context['spacer12'] = self.create_spacers((21,),
                                                              (port.channel_ds_data_rate_profile_num,))[0] * ' '
                    context['spacer13'] = self.create_spacers((13,),
                                                              (port.channel_us_data_rate_profile_num,))[0] * ' '
                    context['spacer14'] = self.create_spacers((13,),
                                                              (port.channel_inp_data_rate_profile_num,))[0] * ' '
                    context['spacer15'] = self.create_spacers((13,), (port.channel_ds_rate_adapt_ratio,))[0] * ' '
                    context['spacer16'] = self.create_spacers((13,), (port.channel_us_rate_adapt_ratio,))[0] * ' '
                    text3 += self._render('display_board_dsl_product_bottom_middle', context=dict(context,
                                                                                                  port=port))

                context['activated_count'] = activated_count
                context['port_counter'] = port_counter - activated_count
                text1 += self._render('display_board_dsl_product_top_bottom', context=context)
                text2 += self._render('display_board_dsl_product_middle_bottom', context=context)
                text3 += self._render('display_board_dsl_product_bottom_bottom', context=context)

                text1 += text2
                text1 += text3

                self._write(text1)

            elif card.product == 'ftth-pon':
                text1 = ''
                text2 = ''
                text3 = ''

                context['spacer1'] = self.create_spacers((18,), (card.power_status,))[0] * ' '
                context['spacer2'] = self.create_spacers((35,), (card.power_off_cause,))[0] * ' '

                text1 += self._render('display_board_ftth_pon_top_top', context=dict(context, card=card))

                ports = self._model.get_ports('card_id', card.id)

                for port in ports:
                    _, _, portname = port.name.split('/')
                    context['portname'] = portname
                    porttype = 'GPON'
                    context['porttype'] = porttype
                    context['spacer_beg1'] = self.create_spacers((5,), (portname,))[0] * ' '
                    context['spacer3'] = self.create_spacers((9,), (porttype,))[0] * ' '
                    context['spacer4'] = self.create_spacers((9,), (port.min_distance,))[0] * ' '
                    context['spacer5'] = self.create_spacers((16,), (port.max_distance,))[0] * ' '
                    context['spacer6'] = self.create_spacers((19,), (port.optical_module_status,))[0] * ' '
                    text1 += self._render('display_board_ftth_pon_top_middle', context=dict(context, port=port))

                    onts = self._model.get_onts('port_id', port.id)

                    ontcounter = 0
                    onlinecounter = 0
                    for ont in onts:
                        if ont.port_id == port.id:
                            ontcounter += 1
                            if ont.admin_state == '1':
                                onlinecounter += 1

                    subrackname, cardportname = port.name.split('/', maxsplit=1)
                    subrackname = subrackname + '/'
                    context['subrackname'] = subrackname
                    context['cardportname'] = cardportname
                    context['ontcounter'] = ontcounter
                    context['onlinecounter'] = onlinecounter

                    if not onts:
                        text2 += self._render('display_board_ftth_pon_ont_summary', context=context)

                    else:
                        text2 += self._render('display_board_ftth_pon_middle_top', context=context)
                        text3 += self._render('display_board_ftth_pon_bottom_top', context=context)
                        for ont in onts:
                            self.map_states(ont, 'ont')
                            context['ont_id'] = ont.index
                            context['spacer_beg2'] = self.create_spacers((4,), (subrackname,))[0] * ' '
                            context['spacer7'] = self.create_spacers((4,), (cardportname,))[0] * ' '
                            context['spacer8'] = self.create_spacers((5,), (ont.index,))[0] * ' '
                            context['spacer9'] = self.create_spacers((18,), (ont.serial_number,))[0] * ' '
                            context['spacer10'] = self.create_spacers((8,), (ont.control_flag,))[0] * ' '
                            context['spacer11'] = self.create_spacers((12,), (ont.admin_state,))[0] * ' '
                            context['spacer12'] = self.create_spacers((9,), (ont.config_state,))[0] * ' '
                            context['spacer13'] = self.create_spacers((8,), (ont.match_state,))[0] * ' '
                            context['spacer14'] = self.create_spacers((4,), ('',))[0] * ' '
                            text2 += self._render('display_board_ftth_pon_middle_middle',
                                                  context=dict(context, ont=ont))

                            context['ont_id'] = ont.index
                            context['spacer_beg3'] = self.create_spacers((4,), (subrackname,))[0] * ' '
                            context['spacer15'] = self.create_spacers((4,), (cardportname,))[0] * ' '
                            context['spacer16'] = self.create_spacers((8,), (ont.index,))[0] * ' '
                            context['spacer17'] = self.create_spacers((3,), ('',))[0] * ' '
                            text3 += self._render('display_board_ftth_pon_bottom_middle',
                                                  context=dict(context, ont=ont))

                        text3 += self._render('display_board_ftth_pon_bottom_bottom', context=context)
                        text3 += self._render('display_board_ftth_pon_ont_summary', context=context)

                text1 += self._render('display_board_ftth_pon_top_bottom', context=context)

                text1 += text2 + text3

                self._write(text1)

            elif card.product == 'ftth' and (card.board_name == 'H802OPGE' or card.board_name == 'H802X2CS'
                                             or card.board_name == 'H806VPEF'):
                text_header = ''
                text_failed = ''
                text_failed_mid = ''
                text1 = ''
                text2 = ''
                text3 = ''
                check = False

                context['spacer1'] = self.create_spacers((18,), (card.power_status,))[0] * ' '
                context['spacer2'] = self.create_spacers((35,), (card.power_off_cause,))[0] * ' '
                text_header += self._render('display_board_ftth_special_header', context=dict(context, card=card))
                text_failed += self._render('display_board_ftth_failed_link_top', context=context)
                text1 += self._render('display_board_ftth_special_top_top', context=context)
                text2 += self._render('display_board_ftth_special_middle_top', context=context)
                text3 += self._render('display_board_ftth_special_bottom_top', context=context)

                ports = self._model.get_ports('card_id', card.id)

                for port in ports:
                    if port.link != 'failed':
                        _, _, portname = port.name.split('/')
                        context['portname'] = portname
                        porttype = ''
                        if port.speed_h == '1000':
                            porttype = 'GE'
                        elif port.speed_h == 'auto_1000':
                            porttype = 'GE'
                        elif port.speed_h == 'auto':
                            porttype = 'GE'
                        elif port.speed_h == '10000':
                            porttype = '10GE'
                        elif port.speed_h == '100000':
                            porttype = '100GE'
                        elif port.speed_h == '100':
                            porttype = 'FE'
                        context['porttype'] = porttype
                        context['spacer_beg1'] = self.create_spacers((6,), (portname,))[0] * ' '
                        context['spacer3'] = self.create_spacers((4,), (porttype,))[0] * ' '
                        context['spacer4'] = self.create_spacers((9,), (port.optic_status,))[0] * ' '
                        context['spacer5'] = self.create_spacers((8,), (port.native_vlan,))[0] * ' '
                        context['spacer6'] = self.create_spacers((2,), ('',))[0] * ' '
                        context['spacer7'] = self.create_spacers((7,), (port.mdi,))[0] * ' '
                        context['spacer8'] = self.create_spacers((10,), (port.speed_h,))[0] * ' '
                        context['spacer9'] = self.create_spacers((10,), (port.duplex,))[0] * ' '
                        context['spacer10'] = self.create_spacers((7,), (port.flow_ctrl,))[0] * ' '
                        context['spacer11'] = self.create_spacers((9,), (port.active_state,))[0] * ' '
                        text1 += self._render('display_board_ftth_special_top_middle',
                                              context=dict(context, port=port))

                        context['spacer_beg2'] = self.create_spacers((6,), (portname,))[0] * ' '
                        context['spacer12'] = self.create_spacers((21,), (port.detecting_time,))[0] * ' '
                        context['spacer13'] = self.create_spacers((2,), ('',))[0] * ' '
                        context['spacer14'] = self.create_spacers((10,), (port.tx_state,))[0] * ' '
                        context['spacer15'] = self.create_spacers((8,), (port.resume_detect,))[0] * ' '
                        context['spacer16'] = self.create_spacers((10,), (port.detect_interval,))[0] * ' '
                        context['spacer17'] = self.create_spacers((22,), (port.resume_duration + port.auto_sensing,
                                                                          ))[0] * ' '
                        text2 += self._render('display_board_ftth_special_middle_middle',
                                              context=dict(context, port=port))

                        context['spacer_beg3'] = self.create_spacers((6,), (portname,))[0] * ' '
                        context['spacer18'] = self.create_spacers((9,), (port.alm_prof_15_min,))[0] * ' '
                        context['spacer19'] = self.create_spacers((9,), (port.warn_prof_15_min,))[0] * ' '
                        context['spacer20'] = self.create_spacers((8,), (port.alm_prof_24_hour,))[0] * ' '
                        context['spacer21'] = self.create_spacers((9,), (port.warn_prof_24_hour,))[0] * ' '
                        text3 += self._render('display_board_ftth_special_bottom_middle',
                                              context=dict(context, port=port))

                    elif port.card_id == card.id and port.link == 'failed':
                        check = True
                        _, _, portname = port.name.split('/')
                        context['portname'] = portname

                        context['spacer_beg_f'] = self.create_spacers((8,), (portname,))[0] * ' '
                        context['spacer_f'] = self.create_spacers((51,), (port.link,))[0] * ' '

                        text_failed_mid += self._render('display_board_ftth_failed_link_middle',
                                                        context=dict(context, port=port))

                text1 += self._render('display_board_ftth_special_top_bottom', context=context)
                text2 += self._render('display_board_ftth_special_middle_bottom', context=context)
                text3 += self._render('display_board_ftth_special_bottom_bottom', context=context)

                if check:
                    text_failed += text_failed_mid
                    text_failed += self._render('display_board_ftth_failed_link_bottom', context=context)
                    text_header += text_failed

                text_header += text1
                text_header += text2
                text_header += text3

                self._write(text_header)

            elif card.product == 'ftth':
                text_header = ''
                text_failed = ''
                text_failed_mid = ''
                text1 = ''
                text2 = ''
                check = False

                text_header += self._render('display_board_ftth_normal_header', context=dict(context, card=card))
                text_failed += self._render('display_board_ftth_failed_link_top', context=context)
                text1 += self._render('display_board_ftth_normal_top_top', context=context)
                text2 += self._render('display_board_ftth_normal_bottom_top', context=context)

                ports = self._model.get_ports('card_id', card.id)

                for port in ports:
                    if port.link != 'failed':
                        _, _, portname = port.name.split('/')
                        porttype = ''
                        if port.speed_h == '1000':
                            porttype = 'GE'
                        elif port.speed_h == 'auto_1000':
                            porttype = 'GE'
                        elif port.speed_h == 'auto':
                            porttype = 'GE'
                        elif port.speed_h == '10000':
                            porttype = '10GE'
                        elif port.speed_h == '100000':
                            porttype = '100GE'
                        elif port.speed_h == '100':
                            porttype = 'FE'
                        context['portname'] = portname
                        context['porttype'] = porttype

                        context['spacer_beg1'] = self.create_spacers((6,), (portname,))[0] * ' '
                        context['spacer1'] = self.create_spacers((3,), (porttype,))[0] * ' '
                        context['spacer2'] = self.create_spacers((3,), ('',))[0] * ' '
                        context['spacer3'] = self.create_spacers((9,), (port.combo_status,))[0] * ' '
                        context['spacer4'] = self.create_spacers((9,), (port.optic_status,))[0] * ' '
                        context['spacer5'] = self.create_spacers((7,), (port.mdi,))[0] * ' '
                        context['spacer6'] = self.create_spacers((11,), (port.speed_h,))[0] * ' '
                        context['spacer7'] = self.create_spacers((10,), (port.duplex,))[0] * ' '
                        context['spacer8'] = self.create_spacers((6,), (port.flow_ctrl,))[0] * ' '
                        context['spacer9'] = self.create_spacers((9,), (port.active_state,))[0] * ' '
                        text1 += self._render('display_board_ftth_normal_top_middle',
                                              context=dict(context, port=port))

                        context['spacer_beg2'] = self.create_spacers((6,), (portname,))[0] * ' '
                        context['spacer10'] = self.create_spacers((9,), (port.alm_prof_15_min,))[0] * ' '
                        context['spacer11'] = self.create_spacers((9,), (port.warn_prof_15_min,))[0] * ' '
                        context['spacer12'] = self.create_spacers((8,), (port.alm_prof_24_hour,))[0] * ' '
                        context['spacer13'] = self.create_spacers((9,), (port.warn_prof_24_hour,))[0] * ' '

                        text2 += self._render('display_board_ftth_normal_bottom_middle',
                                              context=dict(context, port=port))

                    elif port.card_id == card.id and port.link == 'failed':
                        check = True
                        _, _, portname = port.name.split('/')
                        context['portname'] = portname

                        context['spacer_beg_f'] = self.create_spacers((8,), (portname,))[0] * ' '
                        context['spacer_f'] = self.create_spacers((51,), (port.link,))[0] * ' '

                        text_failed_mid += self._render('display_board_ftth_failed_link_middle',
                                                        context=dict(context, port=port))

                text1 += self._render('display_board_ftth_normal_top_bottom', context=context)
                text2 += self._render('display_board_ftth_normal_bottom_bottom', context=context)

                if check:
                    text_failed += text_failed_mid
                    text_failed += self._render('display_board_ftth_failed_link_bottom', context=context)
                    text_header += text_failed

                text_header += text1
                text_header += text2

                self._write(text_header)

            elif card.product == 'mgnt':
                text_header = self._render('display_board_mgnt_header', context=dict(context, card=card))
                text_top = ''
                text_bottom = ''
                text_failed = ''

                text_top += self._render('display_board_mgnt_top_top', context=context)
                text_bottom += self._render('display_board_mgnt_bottom_top', context=context)
                ports = self._model.get_ports('card_id', card.id)
                for port in ports:
                    if port.link == 'failed':
                        text_failed += self._render('display_board_mgnt_failed_top', context=context)

                        _, _, port_num = port.name.split('/')
                        context['port_num'] = port_num
                        port_type = 'AUTO'
                        context['port_type'] = port_type
                        link_down = 'DOWN'
                        context['link_down'] = link_down

                        context['spacer1'] = self.create_spacers((6,), (port_num,))[0] * ' '
                        context['spacer2'] = self.create_spacers((2,), ('',))[0] * ' '
                        context['spacer3'] = self.create_spacers((17,), (port_type,))[0] * ' '
                        text_failed += self._render('display_board_mgnt_failed_mid', context=dict(context, port=port))

                        text_failed += self._render('display_board_mgnt_failed_bottom', context=context)

                    else:
                        port_type = 'GE'
                        _, _, port_num = port.name.split('/')
                        context['port_num'] = port_num
                        context['port_type'] = port_type

                        context['spacer1'] = self.create_spacers((5,), ('',))[0] * ' '
                        context['spacer2'] = self.create_spacers((2,), (port_num,))[0] * ' '
                        context['spacer3'] = self.create_spacers((5,), (port_type,))[0] * ' '
                        context['spacer4'] = self.create_spacers((9,), (port.combo_status,))[0] * ' '
                        context['spacer5'] = self.create_spacers((9,), (port.optic_status,))[0] * ' '
                        context['spacer6'] = self.create_spacers((7,), (port.mdi,))[0] * ' '
                        context['spacer7'] = self.create_spacers((11,), (port.speed_h,))[0] * ' '
                        context['spacer8'] = self.create_spacers((10,), (port.duplex,))[0] * ' '
                        context['spacer9'] = self.create_spacers((6,), (port.flow_ctrl,))[0] * ' '
                        context['spacer10'] = self.create_spacers((9,), (port.active_state,))[0] * ' '
                        text_top += self._render('display_board_mgnt_top_mid', context=dict(context, port=port))

                        context['spacer1'] = self.create_spacers((6,), (port_num,))[0] * ' '
                        context['spacer2'] = self.create_spacers((9,), (port.alm_prof_15_min,))[0] * ' '
                        context['spacer3'] = self.create_spacers((9,), (port.warn_prof_15_min,))[0] * ' '
                        context['spacer4'] = self.create_spacers((8,), (port.alm_prof_24_hour,))[0] * ' '
                        context['spacer5'] = self.create_spacers((9,), (port.warn_prof_24_hour,))[0] * ' '
                        text_bottom += self._render('display_board_mgnt_bottom_mid', context=dict(context, port=port))

                text_top += self._render('display_board_mgnt_top_bottom', context=context)
                text_bottom += self._render('display_board_mgnt_bottom_bottom', context=context)

                try:
                    port_name_0 = card.name + '/0'
                    port_0 = self._model.get_port('name', port_name_0)
                    port_name_1 = card.name + '/1'
                    port_1 = self._model.get_port('name', port_name_1)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if port_0.link == 'failed':
                    text = text_header + text_failed + text_top + text_bottom
                elif port_1.link == 'failed':
                    text = text_header + text_top + text_bottom + text_failed
                else:
                    text = text_header + text_top + text_bottom
                self._write(text)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        return

    def display_service_port(self, command, args, context):
        s_port_idx, = self._dissect(args, 'service-port', str)

        if s_port_idx == 'all':
            if self._model.smart_mode:
                self.user_input('{ <cr>|sort-by<K>||<K> }:')
            text = self._render('display_service_port_all_top', context=context)

            s_ports = self._model.service_ports
            s_port_count = 0
            s_port_up = 0
            s_port_down = 0
            for s_port in s_ports:
                self.map_states(s_port, 'service_port')
                port, card, vlan, porttype = self.prepare_template_vars(s_port, command)

                context['porttype'] = porttype

                sub_idx, card_idx, port_idx = port.name.split('/')
                portname = sub_idx + '/' + card_idx + ' /' + port_idx
                context['portname'] = portname

                context['spacer1'] = self.create_spacers((8,), (s_port.name,))[0] * ' '
                context['spacer2'] = self.create_spacers((5,), (vlan.number,))[0] * ' '
                context['spacer3'] = self.create_spacers((7,), (vlan.attribute,))[0] * ' '
                context['spacer4'] = self.create_spacers((7,), (porttype,))[0] * ' '
                context['spacer5'] = self.create_spacers((7,), (portname,))[0] * ' '
                context['spacer6'] = self.create_spacers((3,), (s_port.vpi,))[0] * ' '
                context['spacer7'] = self.create_spacers((6,), (s_port.vci,))[0] * ' '
                context['spacer8'] = self.create_spacers((9,), (s_port.flow_type,))[0] * ' '
                context['spacer9'] = self.create_spacers((6,), (s_port.flow_para,))[0] * ' '
                context['spacer10'] = self.create_spacers((8,), (s_port.rx,))[0] * ' '
                context['spacer11'] = self.create_spacers((5,), (s_port.tx,))[0] * ' '
                context['spacer12'] = self.create_spacers((7,), (s_port.operational_state,))[0] * ' '

                text += self._render('display_service_port_all_middle',
                                     context=dict(context, port=port, s_port=s_port, vlan=vlan))

                if s_port.operational_state == 'up':
                    s_port_up += 1
                else:
                    s_port_down += 1
                s_port_count += 1

            context['s_port_count'] = s_port_count
            context['s_port_up'] = s_port_up
            context['s_port_down'] = s_port_down
            text += self._render('display_service_port_all_bottom', context=context)

            self._write(text)
            return

        try:
            s_port = self._model.get_service_port('name', s_port_idx)
            self.map_states(s_port, 'service_port')
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

        port, _, vlan, porttype = self.prepare_template_vars(s_port, command)

        context['porttype'] = porttype

        text = self._render(
            'display_service_port',
            context=dict(context, port=port, s_port=s_port, vlan=vlan))
        self._write(text)

        return

    def prepare_template_vars(self, s_port, command):
        if s_port.connected_type == 'port':
            try:
                port = self._model.get_port('id', s_port.connected_id)
                card = self._model.get_card('id', port.card_id)
                s_vlan = self._model.get_service_vlan('service_port_id', s_port.id)
                vlan = self._model.get_vlan('id', s_vlan.vlan_id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif s_port.connected_type == 'ont':
            try:
                ont_port = self._model.get_ont_port('id', s_port.connected_id)
                ont = self._model.get_ont('id', ont_port.ont_id)
                port = self._model.get_port('id', ont.port_id)
                card = self._model.get_card('id', port.card_id)
                s_vlan = self._model.get_service_vlan('service_port_id', s_port.id)
                vlan = self._model.get_vlan('id', s_vlan.vlan_id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif s_port.connected_type == 'cpe':
            try:
                cpe_port = self._model.get_cpe_port('id', s_port.connected_id)
                cpe = self._model.get_cpe('id', cpe_port.cpe_id)
                try:
                    port = self._model.get_port('id', cpe.port_id)
                    card = self._model.get_card('id', port.card_id)
                except exceptions.SoftboxenError:
                    ont_port = self._model.get_ont_port('id', cpe.ont_port_id)
                    ont = self._model.get_ont('id', ont_port.ont_id)
                    port = self._model.get_port('id', ont.port_id)
                    card = self._model.get_card('id', port.card_id)
                s_vlan = self._model.get_service_vlan('service_port_id', s_port.id)
                vlan = self._model.get_vlan('id', s_vlan.vlan_id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

        if card.product == 'vdsl':
            porttype = 'vdl'
        elif card.product == 'adsl':
            porttype = 'adl'
        elif card.product == 'ftth':
            porttype = 'eth'
        elif card.product == 'ftth-pon':
            porttype = 'gpon'
        else:
            raise exceptions.CommandSyntaxError(command=command)

        return port, card, vlan, porttype

    def display_terminal_user(self, command, context):
        text = self._render('display_terminal_user_all_top', context=context)
        user_counter = 0

        try:
            exec_user = self._model.get_user('status', 'online')
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

        for user in self._model.users:
            if (exec_user.level == 'User') and (user.level == 'User'):
                check = True
            elif (exec_user.level == 'Operator') and ((user.level == 'User') or (user.level == 'Operator')):
                check = True
            elif (exec_user.level == 'Admin') and (user.level != 'Super'):
                check = True
            elif exec_user.level == 'Super':
                check = True
            else:
                check = False

            if check:
                context['spacer1'] = self.create_spacers((16,), (user.name,))[0] * ' '
                context['spacer2'] = self.create_spacers((9,), (user.level,))[0] * ' '
                context['spacer3'] = self.create_spacers((15,), (user.status + str(user.reenter_num),))[0] * ' '
                context['spacer4'] = self.create_spacers((1,), ('',))[0] * ' '
                context['spacer5'] = self.create_spacers((16,), (user.profile,))[0] * ' '

                user.status = user.status.capitalize()
                text += self._render('display_terminal_user_all_middle', context=dict(context, user=user))
                user_counter += 1

        context['user_counter'] = user_counter
        text += self._render('display_terminal_user_all_bottom', context=context)
        self._write(text)
        return
