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
from .baseCommandProcessor import BaseCommandProcessor
from .baseMixIn import BaseMixIn


class UserViewCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)


  #########################################################
    def do_exec(self, command, *args, context=None):
        if self._validate(args, str, 'no', 'interactive', 'at-replay', 'continue'):
            file_path, = self._dissect(args, str, 'no', 'interactive', 'at-replay', 'continue')

            # FIXME: currently not implemented
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_info(self, command, *args, context=None):
        if self._validate(args, 'configure', 'bridge', 'port'):
            text = self._render('configure_bridge_port_top', context=context)

            for service_port in self._model.service_ports:
                context['service_port'] = service_port
                context['qos_profile_name'] = None
                if service_port.qos_profile_id is not None:
                    qos_profile = self._model.get_port_profile('id', service_port.qos_profile_id)
                    context['qos_profile_name'] = qos_profile.name
                text += self._render('configure_bridge_port_middle_top', context=context)

                vlans = self._model.get_service_vlans_by_service_port_id(service_port.id)

                for vlan in vlans:
                    context['vlan'] = vlan
                    text += self._render('configure_bridge_port_vlan', context=context)

                text += self._render('configure_bridge_port_middle_bottom', context=context)

            text += self._render('configure_bridge_port_bottom', context=context)
            self._write(text)
        elif self._validate(args, 'configure', 'bridge', 'port', str, 'detail'):
            port_identifier, = self._dissect(args, 'configure', 'bridge', 'port', str, 'detail')

            text = self._render('configure_bridge_port_top', context=context)

            try:
                service_port = self._model.get_service_port('name', port_identifier)
                text += self._render('configure_bridge_port_identifier_detail',
                                     context=dict(context, service_port=service_port))
                context['qos_profile_name'] = None
                if service_port.qos_profile_id is not None:
                    qos_profile = self._model.get_port_profile('id', service_port.qos_profile_id)
                    context['qos_profile_name'] = qos_profile.name
                context['service_port'] = service_port

                service_vlans = self._model.get_service_vlans_by_service_port_id(service_port.id)
                for service_vlan in service_vlans:
                    text += self._render('configure_bridge_port_identifier_detail_vlan',
                                         context=dict(context, service_vlan=service_vlan))
                text += self._render('configure_bridge_port_middle_bottom',
                                     context=dict(context, service_port=service_port))
                text += self._render('configure_bridge_port_bottom', context=context)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            self._write(text)
        elif self._validate(args, 'configure', str, 'line', str):
            product, port_identifier = self._dissect(args, 'configure', str, 'line', str)

            _ = self.command_port_check(product, port_identifier)

            text = self._render('configure_product_line_port', context=dict(context, product=product))
            self._write(text)
        elif self._validate(args, 'configure', 'ethernet', 'line', str, 'detail'):
            port_identifier, = self._dissect(args, 'configure', 'ethernet', 'line', str, 'detail')

            port = self._model.get_port("name", port_identifier)
            context['port'] = port
            card = self._model.get_card("id", port.card_id)
            assert (card.product == 'ftth')

            if port.admin_state == '1':
                context['admin_state'] = "admin-up"
            else:
                context['admin_state'] = "no admin-up"

            ont = self._model.get_ont("port_id", port.id)
            context['mau'] = ont

            text = self._render('configure_ethernet_line_identifier_detail',
                                context=context, ignore_errors=False)
            self._write(text)
        elif self._validate(args, 'configure', str, 'line', str, 'detail'):
            product, port_identifier = self._dissect(args, 'configure', str, 'line', str, 'detail')
            context = dict()

            try:
                port = self._model.get_port("name", port_identifier)
                card = self._model.get_card("id", port.card_id)
                assert (product == 'adsl' or product == 'vdsl' or product == 'xdsl' or product == 'sdsl')
                assert (card.product == product)
                if port.admin_state == '1':
                    context['admin_state'] = "admin-up"
                else:
                    context['admin_state'] = "no admin-up"

                try:
                    port_profiles = []
                    profile_types = ('service', 'spectrum', 'vect', 'dpbo')
                    for profile_type in profile_types:
                        if getattr(port, profile_type+'_profile_id') is None:
                            continue
                        port_profiles.append(self._model.get_port_profile("id",
                                                                          getattr(port, profile_type+'_profile_id')))
                    for profile in port_profiles:
                        context[profile.type + '_profile_id'] = profile.id
                        context[profile.type + '_profile_name'] = profile.name
                except exceptions.InvalidInputError:
                    text = self._render('configure_product_line_port', context=dict(context, product=product))
                    self._write(text)
                    return

            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('configure_product_line_port_detail', context=dict(context, port=port, product=product))
            self._write(text)
        elif self._validate(args, 'configure', 'ethernet', 'line', str, 'mau', '1', 'detail'):
            port_identifier, = self._dissect(args, 'configure', 'ethernet', 'line', str, 'mau', '1', 'detail')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.CommandSyntaxError(command=command)

            ont = self._model.get_ont("port_id", port.id)
            context['index'] = port.name
            context['mau'] = ont
            text = self._render('configure_ethernet_line_identifier_mau_identifier_detail', context=context)
            self._write(text)
        elif self._validate(args, 'configure', 'ethernet', 'ont', str, 'detail'):
            port_identifier, = self._dissect(args, 'configure', 'ethernet', 'ont', str, 'detail')

            try:
                ont_port = self._model.get_ont_port("name", port_identifier)
                self.map_states(ont_port, 'ont_port')
                ont = self._model.get_ont('id', ont_port.ont_id)
                port = self._model.get_port('id', ont.port_id)
                card = self._model.get_card('id', port.card_id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product == "ftth-pon":
                ont_port.uni_idx = port_identifier
                text = self._render('configure_ethernet_ont_ontportidx_detail',
                                    context=dict(context, ont_port=ont_port))
                self._write(text)
        elif self._validate(args, 'configure', 'vlan', 'id', str):
            vlan_id, = self._dissect(args, 'configure', 'vlan', 'id', str)

            try:
                vlan = self._model.get_vlan("number", int(vlan_id))

            except exceptions.InvalidInputError:
                raise exceptions.CommandSyntaxError(command=command)

            text = self._render('configure_vlan_id_vlan_id', context=dict(context, vlan=vlan))
            self._write(text)
        elif self._validate(args, 'configure', 'qos', 'profiles'):
            qos_profiles = self._model.get_port_profiles(params={"type": "qos"})
            policers = self._model.get_port_profiles(params={"type": "policer"})

            context['profiles'] = False

            text = self._render('configure_qos_profiles_session_top', context=context)

            for qos_profile in qos_profiles:
                context['profile'] = qos_profile
                text += self._render('configure_qos_profiles_session_middle', context=context)

            for policer in policers:
                context['policer'] = policer
                text += self._render('configure_qos_profiles_policer_middle', context=context)

            text += self._render('configure_qos_profiles_session_bottom', context=context)

            self._write(text)
        elif self._validate(args, 'configure', 'qos', 'profiles', 'session'):
            qos_profiles = self._model.get_port_profiles(params={"type": "qos"})

            context['profiles'] = True

            text = self._render('configure_qos_profiles_session_top', context=context)

            for qos_profile in qos_profiles:
                context['profile'] = qos_profile
                text += self._render('configure_qos_profiles_session_middle', context=context)

            text += self._render('configure_qos_profiles_session_bottom', context=context)

            self._write(text)
        elif self._validate(args, 'configure', 'qos', 'profiles', 'session', str):
            profile_name, = self._dissect(args, 'configure', 'qos', 'profiles', 'session', str)
            profile = self._model.get_port_profile("name", profile_name)

            if profile.type != 'qos':
                raise exceptions.InvalidInputError

            context['profiles'] = True
            context['profile'] = profile

            text = self._render('configure_qos_profiles_session_top', context=context)
            text += self._render('configure_qos_profiles_session_middle', context=context)
            text += self._render('configure_qos_profiles_session_bottom', context=context)

            self._write(text)

        elif self._validate(args, 'configure', 'vlan'):
            text = self._render('info_configure_vlan_head', context=dict(context, box=self._model))
            try:
                card = self._model.get_card('name', 'nt-a')
            except exceptions.SoftboxenError:
                try:
                    card = self._model.get_card('name', 'nt-b')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            text2 = self._render('info_configure_vlan_shub_top', context=dict(context, card=card))
            for vlan in self._model.vlans:
                if vlan.mode == 'residential-bridge':
                    text += self._render('info_configure_vlan_body', context=dict(context, vlan=vlan))

                text2 += self._render('info_configure_vlan_shub_vlan', context=dict(context, vlan=vlan))
                egress_ports = vlan.egress_port
                if egress_ports.__contains__(','):
                    eports = egress_ports.split(',')[:-1]
                    for eport in eports:
                        context['egress'] = eport
                        text2 += self._render('info_configure_vlan_shub_vlan_egress_port', context=context)
                text2 += self._render('info_configure_vlan_shub_vlan_end', context=context)
            text += text2
            text += self._render('info_configure_vlan_bottom', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class InfoConfigureQosCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

