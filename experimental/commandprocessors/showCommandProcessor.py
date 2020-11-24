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

import re

from nesi import exceptions
from .baseCommandProcessor import BaseCommandProcessor
from .baseMixIn import BaseMixIn


class ShowCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

        ###########################

    def do_software_mngt(self, command, *args, context=None):
        if self._validate(args, 'version', 'etsi', 'detail'):
            text = self._render('software_mngt_version_etsi_detail', context=dict(context, box=self._model))
            self._write(text)

        elif self._validate(args, 'upload-download', 'detail'):
            context['spacer'] = self.create_spacers((27,), (self._model.disk_space,))[0] * ' '
            text = self._render('software_mngt_upload_download_detail', context=dict(context, box=self._model))
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_alarm(self, command, *args, context=None):
        if self._validate(args, 'current', 'table'):
            text = self._render('alarm_current_table_top', context=context)
            text += self._render('alarm_current_table_mid', context=context)
            text += self._render('alarm_current_table_bot', context=dict(context, count=0))
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def product(self, command, *args, context=None):
        if self._validate(args, '?'):
            text = self._render('product_help', context=context)
            self._write(text)
        elif self._validate(args, 'operational-data', '?'):
            text = self._render('product_operational_data_help', context=context)
            self._write(text)
        elif self._validate(args, 'operational-data', 'line', '?'):
            text = self._render('product_operational_data_line_help', context=context)
            self._write(text)
        elif self._validate(args, 'operational-data', 'line', str, 'detail', '?'):
            text = self._render('product_operational_data_line_port_detail_help', context=context)
            self._write(text)
        elif self._validate(args, 'operational-data', 'line', str, 'detail'):
            port_identifier, = self._dissect(args, 'operational-data', 'line', str, 'detail')

            port = self.command_port_check(command, port_identifier)

            context['spacer1'] = self.create_spacers((29,), (port.name, port.admin_state))[0] * ' '
            context['spacer2'] = self.create_spacers((28,), (port.operational_state, port.upstream))[0] * ' '
            context['spacer3'] = self.create_spacers((24,), (port.downstream, port.upstream_max))[0] * ' '
            context['spacer4'] = self.create_spacers((32,), (port.downstream_max, port.upstream_max))[0] * ' '
            context['spacer5'] = self.create_spacers((29,), (port.inp_dn, port.upstream_max))[0] * ' '
            context['spacer6'] = self.create_spacers((27,), (port.interl_dn, port.upstream_max))[0] * ' '
            context['spacer7'] = self.create_spacers((20,), (port.rinit_1d, port.upstream_max))[0] * ' '
            context['spacer8'] = self.create_spacers((27,), (port.rtx_mode_up, port.upstream_max))[0] * ' '
            context['spacer9'] = self.create_spacers((17,), (port.total_reset_attempt, port.upstream_max))[0] * ' '

            text = self._render('product_operational_data_line_port_detail', context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'linkup-record', str, 'detail'):
            port_identifier, = self._dissect(args, 'linkup-record', str, 'detail')

            port = self.command_port_check(command, port_identifier)

            context['spacer1'] = self.create_spacers((21,), (port.upstream,))[0] * ' '
            context['spacer2'] = self.create_spacers((16,), (port.noise_margin_up,))[0] * ' '
            context['spacer3'] = self.create_spacers((21,), (port.attenuation_up,))[0] * ' '
            context['spacer4'] = self.create_spacers((16,), (port.attained_upstream,))[0] * ' '
            context['spacer5'] = self.create_spacers((21,), (port.upstream_max,))[0] * ' '
            context['spacer6'] = self.create_spacers((15,), (port.threshold_upstream,))[0] * ' '
            context['spacer7'] = self.create_spacers((23,), (port.max_delay_upstream,))[0] * ' '
            context['spacer8'] = self.create_spacers((16,), (port.tgt_noise_margin_up,))[0] * ' '

            text = self._render('product_linkuprecord_port_detail', context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'cpe-inventory', str, 'detail'):
            port_identifier, = self._dissect(args, 'cpe-inventory', str, 'detail')

            port = self.command_port_check(command, port_identifier)

            text = self._render('product_cpeinventory_port_detail',
                                context=dict(context, port=port))
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_adsl(self, command, *args, context=None):
        self.product(command, *args, context=context)

    def do_sdsl(self, command, *args, context=None):
        self.product(command, *args, context=context)

    def do_vdsl(self, command, *args, context=None):
        self.product(command, *args, context=context)

    def do_xdsl(self, command, *args, context=None):
        self.product(command, *args, context=context)

    def do_equipment(self, command, *args, context=None):
        if self._validate(args, 'shelf', str, 'detail'):
            subrack_id, = self._dissect(args, 'shelf', str, 'detail')

            try:
                subrack = self._model.get_subrack("name", subrack_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((25,), (subrack.name, ))[0] * ' '
            context['spacer2'] = self.create_spacers((26,), (subrack.actual_type,))[0] * ' '
            text = self._render('equipment_shelf_shelfid_detail', context=dict(context, subrack=subrack))
            self._write(text)
        elif self._validate(args, 'slot', str, 'detail'):
            lt_identifier, = self._dissect(args, 'slot', str, 'detail')

            if lt_identifier == 'nt-a' or lt_identifier == 'nt-b' or lt_identifier == 'acu:1/1':
                try:
                    card = self._model.get_card('name', lt_identifier)

                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                context['spacer1'] = self.create_spacers((26,), (card.name,))[0] * ' '
                context['spacer2'] = self.create_spacers((26,), (card.actual_type,))[0] * ' '
                context['slot_name'] = lt_identifier

                text = self._render('equipment_slot_slotid_detail', context=dict(context, card=card))

            else:
                if not lt_identifier.startswith('lt:'):
                    lt_identifier = 'lt:' + lt_identifier
                    
                try:
                    card = self._model.get_card("position", lt_identifier)
                    assert (card.product == 'ftth-pon' or card.product == 'ftth' or card.product == 'adsl' or
                            card.product == 'xdsl' or card.product == 'vdsl' or card.product == 'sdsl')
                except (exceptions.SoftboxenError, AssertionError):
                    raise exceptions.CommandSyntaxError(command=command)

                context['slot_name'] = card.position
                context['spacer1'] = self.create_spacers((25,), (context['slot_name'], ))[0] * ' '
                context['spacer2'] = self.create_spacers((26,), (card.actual_type,))[0] * ' '

                text = self._render('equipment_slot_slotid_detail', context=dict(context, card=card))
            self._write(text)
        elif self._validate(args, 'slot', 'detail'):
            text = self._render('equipment_slot_detail_head', context=context)

            for card in self._model.cards:
                if card.position == 'network:0':
                    context['spacer1'] = self.create_spacers((25,), (card.name, ))[0] * ' '
                else:
                    context['spacer1'] = self.create_spacers((25,), (card.position,))[0] * ' '
                context['spacer2'] = self.create_spacers((26,), (card.actual_type,))[0] * ' '
                text += self._render('equipment_slot_detail_body', context=dict(context, card=card))
            self._write(text)
        elif self._validate(args, 'slot'):
            text = self._render('equipment_slot_top', context=context)
            cards = []
            for card in self._model.cards:
                if 'nt' in card.name:
                    cards.insert(0, card)
                else:
                    cards.append(card)

            for card in cards:
                context['slot_name'] = card.position

                enabled = 'no'

                if card.operational_state == '1':
                    enabled = 'yes'

                args = (context['slot_name'], card.actual_type, enabled, card.err_state, card.availability,
                        card.restrt_cnt)
                positions = (10, 22, 30, 53, 67)
                spacers = self.create_spacers(positions, args)

                context['spacer1'] = spacers[0] * ' '
                context['spacer2'] = spacers[1] * ' '
                context['spacer3'] = spacers[2] * ' '
                context['spacer4'] = spacers[3] * ' '
                context['spacer5'] = spacers[4] * ' '
                text += self._render('equipment_slot_middle', context=dict(context, card=card))

            context['totalcards'] = self._model.cards.__len__()
            text += self._render('equipment_slot_bottom', context=context)
            self._write(text)
        elif self._validate(args, 'diagnostics', 'sfp', str, 'detail'):
            port_identifier, = self._dissect(args, 'diagnostics', 'sfp', str, 'detail')

            try:
                port = self._model.get_port("position", port_identifier)
                card = self._model.get_card("id", port.card_id)
                assert(card.product == 'ftth-pon')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((29,), (port.los,))[0] * ' '
            context['spacer2'] = self.create_spacers((27,), (port.rssi_profile_id,))[0] * ' '
            text = self._render('equipment_diagnostics_sfp_sfpport_detail', context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'ont', 'interface', str, 'detail'):
            port_identifier, = self._dissect(args, 'ont', 'interface', str, 'detail')

            try:
                ont = self._model.get_ont("name", port_identifier)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((25,), (ont.name,))[0] * ' '
            context['spacer2'] = self.create_spacers((27,), (ont.sw_ver_act,))[0] * ' '
            context['spacer3'] = self.create_spacers((23,), (ont.actual_num_slots,))[0] * ' '
            context['spacer4'] = self.create_spacers((24,), (ont.num_tconts,))[0] * ' '
            context['spacer5'] = self.create_spacers((18,), (ont.num_prio_queues,))[0] * ' '
            context['spacer6'] = self.create_spacers((31,), (ont.auto_sw_download_ver,))[0] * ' '
            context['spacer7'] = self.create_spacers((25,), (ont.oper_spec_ver,))[0] * ' '
            context['spacer8'] = self.create_spacers((21,), (ont.act_txpower_ctrl,))[0] * ' '
            context['spacer9'] = self.create_spacers((21,), (ont.cfgfile1_ver_act,))[0] * ' '
            context['spacer10'] = self.create_spacers((21,), (ont.cfgfile2_ver_act,))[0] * ' '
            text = self._render('equipment_ont_interface_ontportidx_detail', context=dict(context, ont=ont))
            self._write(text)
        elif self._validate(args, 'ont', 'optics', str, 'detail'):
            port_identifier, = self._dissect(args, 'ont', 'optics', str, 'detail')

            try:
                ont = self._model.get_ont("name", port_identifier)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((22,), (ont.name,))[0] * ' '
            context['spacer2'] = self.create_spacers((22,), (ont.tx_signal_level,))[0] * ' '
            context['spacer3'] = self.create_spacers((22,), (ont.ont_voltage,))[0] * ' '
            text = self._render('equipment_ont_optics_ontportidx_detail', context=dict(context, ont=ont))
            self._write(text)
        elif self._validate(args, 'ont', 'operational-data', str, 'detail'):
            port_identifier, = self._dissect(args, 'ont', 'operational-data', str, 'detail')

            try:
                ont = self._model.get_ont("name", port_identifier)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((23,), (ont.name, ))[0] * ' '
            context['spacer2'] = self.create_spacers((26,), (ont.loss_of_ack, ))[0] * ' '
            context['spacer3'] = self.create_spacers((22,), (ont.physical_eqpt_err, ))[0] * ' '
            context['spacer4'] = self.create_spacers((25,), (ont.signal_degrade,))[0] * ' '
            context['spacer5'] = self.create_spacers((29,), (ont.msg_error_msg,))[0] * ' '
            context['spacer6'] = self.create_spacers((26,), (ont.loss_of_frame,))[0] * ' '
            context['spacer7'] = self.create_spacers((22,), (ont.dying_gasp,))[0] * ' '
            context['spacer8'] = self.create_spacers((22,), (ont.loss_of_ploam,))[0] * ' '
            context['spacer9'] = self.create_spacers((21,), (ont.remote_defect_ind,))[0] * ' '
            context['spacer10'] = self.create_spacers((27,), (ont.rogue_ont_disabled,))[0] * ' '
            text = self._render('equipment_ont_operational-data_ontportidx_detail', context=dict(context, ont=ont))
            self._write(text)
        elif self._validate(args, 'temperature'):
            text = self._render('equipment_temperature_top', context=context)
            for card in self._model.cards:
                context['ident'] = card.name
                context['spacer1'] = self.create_spacers((10,), (context['ident'],))[0] * ' '
                context['spacer2'] = self.create_spacers((10,), (card.sensor_id,))[0] * ' '
                context['spacer3'] = self.create_spacers((11,), (card.act_temp,))[0] * ' '
                context['spacer4'] = self.create_spacers((11,), (card.tca_low,))[0] * ' '
                context['spacer5'] = self.create_spacers((11,), (card.tca_high,))[0] * ' '
                context['spacer6'] = self.create_spacers((11,), (card.shut_low,))[0] * ' '
                text += self._render('equipment_temperature_middle', context=dict(context, card=card))
            text += self._render('equipment_temperature_bottom',
                                 context=dict(context, count=self._model.cards.__len__()))
            self._write(text)
        elif self._validate(args, 'transceiver-inventory', str, 'detail'):
            port_identifier, = self._dissect(args, 'transceiver-inventory', str, 'detail')

            try:
                port = self._model.get_port("position", port_identifier)
                card = self._model.get_card("id", port.card_id)
                assert card.product == 'ftth'
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('equipment_transceiver_inventory_identifier_detail',
                                context=dict(context, port=port, card=card))
            self._write(text)
        elif self._validate(args, 'transceiver-inventory'):
            text = self._render('equipment_transceiver_inventory_identifier_top', context=context)
            count = 0
            try:
                for port in self._model.ports:
                    card = self._model.get_card("id", port.card_id)
                    if card.actual_type == 'fant-f' and not port.name.endswith(':32'):
                        count += 1
                        context['spacer1'] = self.create_spacers((25,), (port.position,))[0] * ' '
                        context['spacer2'] = self.create_spacers((19,), (port.inventory_status,))[0] * ' '
                        context['spacer3'] = self.create_spacers((64,), (port.alu_part_num,))[0] * ' '
                        context['spacer4'] = self.create_spacers((64,), (port.tx_wavelength,))[0] * ' '
                        context['spacer5'] = self.create_spacers((14,), (port.fiber_type,))[0] * ' '
                        text += self._render('equipment_transceiver_inventory_identifier_mid',
                                             context=dict(context, port=port))

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            text += self._render('equipment_transceiver_inventory_identifier_bottom',
                                 context=dict(context, count=count))
            self._write(text)
        elif self._validate(args, 'shelf', 'detail'):
            text = self._render('equipment_shelf_detail_head', context=context)

            counter = 0
            for subrack in self._model.subracks:
                context['subrack'] = subrack
                context['spacer'] = self.create_spacers((25,), (subrack.actual_type,))[0] * ' '
                text += self._render('equipment_shelf_detail_body', context=context)
                counter += 1

            text += self._render('equipment_shelf_detail_bottom', context=context)
            self._write(text)

        elif self._validate(args, 'shelf'):
            text = self._render('equipment_shelf_top', context=context)

            counter = 0
            for subrack in self._model.subracks:
                enabled = 'no'

                if subrack.operational_state == '1':
                    enabled = 'yes'
                context['subrack'] = subrack
                context['enabled'] = enabled
                context['spacer1'] = self.create_spacers((6,), (subrack.name,))[0] * ' '
                context['spacer2'] = self.create_spacers((12,), (subrack.actual_type,))[0] * ' '
                context['spacer3'] = self.create_spacers((8,), (enabled,))[0] * ' '
                context['spacer4'] = self.create_spacers((23,), (subrack.err_state,))[0] * ' '
                text += self._render('equipment_shelf_body', context=context)
                counter += 1

            context['counter'] = counter
            text += self._render('equipment_shelf_bottom', context=context)
            self._write(text)

        elif self._validate(args, 'ont', 'slot', 'detail'):
            text = self._render('equipment_ont_slot_detail_top', context=context)

            for ont in self._model.onts:
                context['spacer1'] = self.create_spacers((18,), (ont.act_num_data_ports,))[0] * ' '
                context['spacer2'] = self.create_spacers((21,), (ont.actual_card_type,))[0] * ' '
                context['spacer3'] = self.create_spacers((19,), (ont.actual_serial_num,))[0] * ' '
                text += self._render('equipment_ont_slot_detail_middle', context=dict(context, ont=ont))

            text += self._render('equipment_ont_slot_detail_bottom', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ethernet(self, command, *args, context=None):
        if self._validate(args, 'ont', 'operational-data', str, 'detail'):
            port_identifier, = self._dissect(args, 'ont', 'operational-data', str, 'detail')

            try:
                ont_port = self._model.get_ont_port("name", port_identifier)
                ont = self._model.get_ont('id', ont_port.ont_id)
                port = self._model.get_port('id', ont.port_id)
                card = self._model.get_card('id', port.card_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product == "ftth-pon":
                ont_port.uni_idx = port_identifier
                context['spacer1'] = self.create_spacers((26,), (ont_port.config_indicator,))[0] * ' '
                text = self._render('ethernet_ont_operational_data_ontportidx_detail',
                                    context=dict(context, ont_port=ont_port))
                self._write(text)
        elif self._validate(args, 'mau'):
            maus = self._model.onts

            mau_count = 0
            text = self._render('ethernet_mau_top', context=context)
            for mau in maus:
                port = self._model.get_port("id", mau.port_id)

                context['if_index'] = port.name
                context['mau'] = mau

                spacers = self.create_spacers(
                    (11, 22, 36, 53, 66, 85),
                    (port.name, mau.index, mau.type, mau.media_available,
                     mau.jabber_state, mau.auto_neg_supported, mau.auto_neg_status)
                )

                i = 1
                for spacer in spacers:
                    context['spacer' + str(i)] = spacer * ' '
                    i += 1

                text += self._render('ethernet_mau_middle', context=context)
                mau_count += 1

            context['mau_count'] = mau_count

            text += self._render('ethernet_mau_bottom', context=context)
            self._write(text)
        elif self._validate(args, 'mau', str, 'detail'):
            port_identifier, = self._dissect(args, 'mau', str, 'detail')
            port = self._model.get_port("name", port_identifier)

            card = self._model.get_card("id", port.card_id)

            if card.product != 'ftth':
                raise exceptions.InvalidInputError

            mau = self._model.get_ont("port_id", port.id)

            context['if_index'] = port.name
            context['template_type'] = 'mau'

            self.fill_mau_template_context(mau, context)

            text = self._render('ethernet_mau_port_detail', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_interface(self, command, *args, context=None):
        if self._validate(args, 'port', '|', 'match', 'match', str):
            port_idx, = self._dissect(args, 'port', '|', 'match', 'match', str)
            pre_statement = port_idx.split(':')[0]  # 'exact'
            if pre_statement == 'exact':
                post_statement_list = port_idx.split(':')[1:]
                if post_statement_list[0] == 'xdsl-line':
                    card_name = str(post_statement_list[1])
                    try:
                        card = self._model.get_card('name', card_name)
                    except exceptions.SoftboxenError:
                        text = self._render('instance_does_not_exist', context=context)
                        self._write(text)
                        return

                    if card.product != 'xdsl':
                        raise exceptions.CommandSyntaxError(command=command)

                    text = ''
                    for port in self._model.ports:
                        if port.card_id == card.id:
                            context['port_ident'] = port.name
                            context['spacer1'] = self.create_spacers((40,), (port.name,))[0] * ' '
                            context['spacer2'] = self.create_spacers((13,), (port.admin_state,))[0] * ' '
                            text += self._render('interface_port_pipe_match_match_exact_product_line_port',
                                                 context=dict(context, port=port, card=card))

                    self._write(text)

                elif post_statement_list[0] == 'ethernet-line':
                    card_name = str(post_statement_list[1])
                    try:
                        card = self._model.get_card('name', card_name)
                    except exceptions.SoftboxenError:
                        text = self._render('instance_does_not_exist', context=context)
                        self._write(text)
                        return

                    if card.product != 'ftth':
                        raise exceptions.CommandSyntaxError(command=command)

                    text = ''
                    card.product = 'ethernet'
                    for port in self._model.ports:
                        if port.card_id == card.id:
                            context['port_ident'] = port.name
                            context['spacer1'] = self.create_spacers((36,), (port.name,))[0] * ' '
                            context['spacer2'] = self.create_spacers((13,), (port.admin_state,))[0] * ' '
                            text += self._render('interface_port_pipe_match_match_exact_product_line_port',
                                                 context=dict(context, port=port, card=card))

                    self._write(text)

                elif re.match("[0-9]+/[0-9]+/[0-9]+/[0-9]+", post_statement_list[0]):
                    slot_idx = self._dissect(post_statement_list, str)
                    port_name = slot_idx[0]
                    text = ''
                    text_pvc = ''
                    text_s_port = ''

                    try:
                        port = self._model.get_port('name', port_name)
                    except exceptions.SoftboxenError:
                        text = self._render('instance_does_not_exist', context=context)
                        self._write(text)
                        return

                    for component in self._model.ports:
                        if port.name in component.name:
                            try:
                                card = self._model.get_card('id', component.card_id)
                            except exceptions.SoftboxenError:
                                text = self._render('instance_does_not_exist', context=context)
                                self._write(text)
                                return
                            if card.product == 'xdsl' or card.product == 'adsl' or card.product == 'vdsl'\
                                    or card.product == 'sdsl':
                                card_product = card.product + '-line'
                            elif card.product == 'ftth':
                                card_product = 'ethernet-line'
                            elif card.product == 'ftth-pon':
                                card_product = 'pon'
                            else:
                                raise exceptions.CommandSyntaxError(command=command)

                            component_indent = card_product + ':' + component.name
                            context['object_type'] = card_product
                            context['component_name'] = component.name
                            context['component_admin_state'] = component.admin_state
                            context['component_operational_state'] = component.operational_state
                            context['spacer1'] = self.create_spacers((52,), (component_indent,))[0] * ' '
                            context['spacer2'] = self.create_spacers((13,), (component.admin_state,))[0] * ' '

                            text += self._render('interface_port_pipe_match_match_exact_port', context=context)

                    for component in self._model.service_ports:
                        if port.name in component.name:
                            if component.pvc:
                                component_indent = 'atm-pvc:' + component.name
                                context['object_type'] = 'atm-pvc'
                                context['component_name'] = component.name
                                context['component_admin_state'] = component.admin_state
                                context['component_operational_state'] = component.operational_state
                                context['spacer1'] = self.create_spacers((52,), (component_indent,))[0] * ' '
                                context['spacer2'] = self.create_spacers((13,), (component.admin_state,))[0] * ' '

                                text_pvc += self._render('interface_port_pipe_match_match_exact_port', context=context)
                            else:
                                component_indent = 'bridge-port:' + component.name
                                context['object_type'] = 'bridge-port'
                                context['component_name'] = component.name
                                context['component_admin_state'] = component.admin_state
                                context['component_operational_state'] = component.operational_state
                                context['spacer1'] = self.create_spacers((52,), (component_indent,))[0] * ' '
                                context['spacer2'] = self.create_spacers((13,), (component.admin_state,))[0] * ' '

                                text_s_port += self._render('interface_port_pipe_match_match_exact_port',
                                                            context=context)

                    text += text_pvc + text_s_port
                    self._write(text)

                else:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'port', str, 'detail'):
            port_identifier, = self._dissect(args, 'port', str, 'detail')

            try:
                port_type, port_identifier = port_identifier.split(':')
                port = self._model.get_port("name", port_identifier)
                card = self._model.get_card("id", port.card_id)
                if port_type == 'pon':
                    assert card.product == 'ftth-pon'
                elif port_type == 'ethernet-line':
                    assert card.product == 'ftth'
                else:
                    assert False
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            context['spacer1'] = self.create_spacers((20,), (port.high_speed,))[0] * ' '
            context['spacer2'] = self.create_spacers((20,), (port.largest_pkt_size,))[0] * ' '
            context['spacer3'] = self.create_spacers((27,), (port.admin_state,))[0] * ' '
            context['spacer4'] = self.create_spacers((19,), (port.last_chg_opr_stat,))[0] * ' '
            context['spacer5'] = self.create_spacers((27,), (port.in_octets,))[0] * ' '
            context['spacer6'] = self.create_spacers((23,), (port.in_ucast_pkts,))[0] * ' '
            context['spacer7'] = self.create_spacers((23,), (port.in_mcast_pkts,))[0] * ' '
            context['spacer8'] = self.create_spacers((19,), (port.in_broadcast_pkts,))[0] * ' '
            context['spacer9'] = self.create_spacers((21,), (port.in_discard_pkts,))[0] * ' '
            context['spacer10'] = self.create_spacers((25,), (port.in_err_pkts,))[0] * ' '

            text = self._render('interface_port_ponport_detail', context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'port'):
            self._write(self._render('interface_port_top', context=context))
            context['count'] = 0
            for port in self._model.ports:
                card = self._model.get_card("id", port.card_id)
                if card.product == 'ftth':
                    context['port_type'] = 'ethernet-line'
                elif card.product == 'ftth-pon':
                    context['port_type'] = 'pon'
                else:
                    context['port_type'] = card.product + '-line'

                positions = (52, 65)
                args = (context['port_type'] + ":" + port.name, port.admin_state, port.operational_state)
                spacers = self.create_spacers(positions, args)

                context['spacer1'] = spacers[0] * ' '
                context['spacer2'] = spacers[1] * ' '
                self._write(self._render('interface_port_middle', context=dict(context, port=port)))
                context['count'] += 1

            for ont in self._model.onts:
                positions = (48, 61)
                args = (ont.name, ont.admin_state, ont.operational_state)
                spacers = self.create_spacers(positions, args)
                context['port_type'] = 'ont'
                context['spacer1'] = spacers[0] * ' '
                context['spacer2'] = spacers[1] * ' '
                self._write(self._render('interface_port_middle', context=dict(context, port=ont)))
                context['count'] += 1

            self._write(self._render('interface_port_bottom', context=context))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shdsl(self, command, *args, context=None):
        if self._validate(args, 'span-status', str, 'detail'):
            port_identifier, = self._dissect(args, 'span-status', str, 'detail')
            try:
                model = self._model.get_port("name", port_identifier)
                card = self._model.get_card("id", model.card_id)
                assert card.product == 'sdsl'
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('shdsl_span_status_port_detail', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vlan(self, command, *args, context=None):
        if self._validate(args, 'bridge-port-fdb'):
            text = self._render('vlan_bridge_port_fdb_top', context=context)
            cpes = []
            count = 0
            for service_port in self._model.service_ports:
                if service_port.connected_type == 'port':
                    port = self._model.get_port('id', service_port.connected_id)
                    cpes = self._model.get_cpes('port_id', port.id)
                elif service_port.connected_type == 'ont':
                    ont_port = self._model.get_ont_port('id', service_port.connected_id)
                    cpes = self._model.get_cpes('ont_port_id', ont_port.id)

                service_vlans = self._model.get_service_vlans('service_port_id', service_port.id)

                for service_vlan in service_vlans:
                    if service_vlan.l2fwder_vlan != '' and service_vlan.l2fwder_vlan is not None:
                        context['vlan_id'] = service_vlan.name
                        context['fdb_id'] = service_vlan.l2fwder_vlan
                    if 'PPPoE' in self._model.get_vlan('id', service_vlan.vlan_id).name:
                        context['vlan_id'] = service_vlan.name
                        context['fdb_id'] = service_vlan.name
                        break

                for cpe in cpes:
                    context['service_port'] = service_port
                    context['cpe_mac'] = cpe.mac
                    count += 1

                    spacers = self.create_spacers([20, 37, 55, 72], [service_port.name, context['vlan_id'], cpe.mac, context['fdb_id']])
                    context['spacer1'] = spacers[0] * ' '
                    context['spacer2'] = spacers[1] * ' '
                    context['spacer3'] = spacers[2] * ' '
                    context['spacer4'] = spacers[3] * ' '

                    text += self._render('vlan_bridge_port_fdb_middle', context=context)

            text += self._render('vlan_bridge_port_fdb_bottom',
                                 context=dict(context, bridgeportcount=count))
            self._write(text)

        elif self._validate(args, 'bridge-port-fdb', str, 'detail'):
            port_identifier, = self._dissect(args, 'bridge-port-fdb', str, 'detail')

            try:
                service_port = self._model.get_service_port('name', port_identifier)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            cpe = None
            if service_port.connected_type == 'port':
                port = self._model.get_port('id', service_port.connected_id)
                cpe = self._model.get_cpe('port_id', port.id)
            elif service_port.connected_type == 'ont':
                ont_port = self._model.get_ont_port('id', service_port.connected_id)
                cpe = self._model.get_cpe('ont_port_id', ont_port.id)

            service_vlans = self._model.get_service_vlans('service_port_id', service_port.id)

            for service_vlan in service_vlans:
                if service_vlan.l2fwder_vlan != '' and service_vlan.l2fwder_vlan is not None:
                    context['vlan_id'] = service_vlan.name
                    context['fdb_id'] = service_vlan.l2fwder_vlan
                if 'PPPoE' in self._model.get_vlan('id', service_vlan.vlan_id).name:
                    context['vlan_id'] = service_vlan.name
                    context['fdb_id'] = service_vlan.name
                    break

            context['service_port'] = service_port
            if cpe is not None:
                context['cpe_mac'] = cpe.mac

            text = self._render('vlan_bridge_port-fdb_ontportidx_detail_top', context=context)
            text += self._render('vlan_bridge_port-fdb_ontportidx_detail_mid', context=context)
            text += self._render('vlan_bridge_port-fdb_ontportidx_detail_bottom', context=context)
            self._write(text)
        elif self._validate(args, 'name'):
            text = self._render('vlan_name_top', context=context)

            vlans = self._model.vlans

            for vlan in vlans:
                context['spacer1'] = self.create_spacers((63,), (vlan.name,))[0] * ' '
                text += self._render('vlan_name_middle', context=dict(context, vlan=vlan))
            text += self._render('vlan_name_bottom', context=dict(context, vlancount=len(vlans)))
            self._write(text)

        elif self._validate(args, 'name', str, 'detail'):
            vlan_name, = self._dissect(args, 'name', str, 'detail')

            try:
                vlan = self._model.get_vlan('name', vlan_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('vlan_name_name_detail', context=dict(context, vlan=vlan))
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_transport(self, command, *args, context=None):
        if self._validate(args, 'ether-ifmault', str, 'detail'):
            port_identifier, = self._dissect(args, 'ether-ifmault', str, 'detail')
            context['if_index'] = port_identifier
            context['template_type'] = 'ether-ifmault'

            port = self._model.get_port("name", port_identifier)

            card = self._model.get_card("id", port.card_id)

            if card.product != 'ftth':
                raise exceptions.InvalidInputError

            mau = self._model.get_ont("port_id", port.id)

            self.fill_mau_template_context(mau, context)

            text = self._render('ethernet_mau_port_detail', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pon(self, command, *args, context=None):
        if self._validate(args, 'unprovision-onu', 'detail'):
            text = self._render('pon_unprovision_onu_detail_top', context=context)

            for ont in self._model.onts:
                if ont.actual_card_type == 'pon' and not ont.provision:
                    port = self._model.get_port('id', ont.port_id)
                    text += self._render('pon_unprovision_onu_detail_middle', context=dict(context, ont=ont, port=port))

            text += self._render('pon_unprovision_onu_detail_bottom', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_linetest(self, command, *args, context=None):
        if self._validate(args, 'single', 'lineid-ext-rept', str):
            session_id, = self._dissect(args, 'single', 'lineid-ext-rept', str)

            if context['meltStart']:
                if session_id == context['session_id']:
                    context['spacer1'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer2'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer3'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer4'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer5'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer6'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer7'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer8'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer9'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer10'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer11'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer12'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer13'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer14'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer15'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer16'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer17'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer18'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer19'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer20'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer21'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer22'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer23'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer24'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '
                    context['spacer25'] = self.create_spacers((10,), (context['session_id'],))[0] * ' '
                    context['spacer26'] = self.create_spacers((14,), (context['port_identifier'],))[0] * ' '

                    text = self._render('linetest_single_lineid_ext_rept_filled', context=context)

                else:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                text = self._render('linetest_single_lineid_ext_rept_empty', context=context)

            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ShowEquipmentTranceiverInventoryPortCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
