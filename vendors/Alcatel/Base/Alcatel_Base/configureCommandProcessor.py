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


class ConfigureCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        if self._validate(command, '?'):
            text = self._render('?', context=context)
            self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_atm(self, command, *args, context=None):
        if self._validate(args, 'pvc', str):
            port_identifier, = self._dissect(args, 'pvc', str)
            try:
                port_idx, _, _ = port_identifier.split(':')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            try:
                port = self._model.get_port('name', port_idx)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                s_port = self._model.get_service_port('name', port_identifier)
            except exceptions.SoftboxenError:
                self._model.add_service_port(name=port_identifier, connected_id=port.id, connected_type='port', admin_state='down', pvc=True)

            return

        elif self._validate(args[:3], 'pvc', str, str):
            port_identifier, admin_prefix = self._dissect(args[:3], 'pvc', str, str)

            try:
                port_idx, _, _ = port_identifier.split(':')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            try:
                port = self._model.get_port('name', port_idx)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                s_port = self._model.get_service_port('name', port_identifier)
            except exceptions.SoftboxenError:
                if admin_prefix == 'no' and args[3] == 'admin-down':
                    self._model.add_service_port(name=port_identifier, connected_id=port.id, connected_type='port', admin_state='up', pvc=True)
                elif admin_prefix == 'admin-down':
                    self._model.add_service_port(name=port_identifier, connected_id=port.id, connected_type='port', admin_state='down', pvc=True)
                else:
                    raise exceptions.CommandSyntaxError(command=command)
                return

            if admin_prefix == 'no' and args[3] == 'admin-down':
                s_port.set_admin_state('up')
            elif admin_prefix == 'admin-down':
                s_port.set_admin_state('down')
            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_interface(self, command, *args, context=None):
        if self._validate(args[:2], 'port', str):
            port_identifier, = self._dissect(args[:2], 'port', str)
            product, port_idx = port_identifier.split(':')
            context['product'] = product

            product_type = None

            if '-line' in product:
                product_type = product.split("-")[0]
                if product_type == 'ethernet':
                    product_type = 'ftth'
            elif product == 'pon':
                product_type = 'ftth-pon'
            elif product == 'uni':
                product_type = '/'

            if product_type != '/':
                try:
                    port = self._model.get_port("name", port_idx)
                    card = self._model.get_card("id", port.card_id)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if card.product != product_type:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                try:
                    ont_port = self._model.get_ont_port('name', port_idx)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                cpe_check = None
                for cpe in self._model.cpes:
                    if cpe.ont_port_id == ont_port.id:
                        cpe_check = cpe
                        break
                if cpe_check is None:
                    raise exceptions.CommandSyntaxError(command=command)

            context['port_idx'] = port_idx
            context['product'] = product
            self.process(ConfigureInterfacePortCommandProcessor, 'login', 'mainloop', 'configure',
                         'interface', 'port', args=args[2:], return_to=ConfigureCommandProcessor,
                         context=context)

        elif self._validate(args, 'shub', 'port', str, 'port-type', 'network', 'mode', 'automatic', 'admin-status',
                            'auto-up'):
            try:
                card = self._model.get_card('name', 'nt-a')
            except exceptions.SoftboxenError:
                try:
                    card = self._model.get_card('name', 'nt-b')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            card.set_admin_state('unlock')

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_equipment(self, command, *args, context=None):
        if self._validate(args, 'ont', 'interface', str, 'admin-state', str):
            ont_identifier, case = self._dissect(args, 'ont', 'interface', str, 'admin-state', str)
            try:
                port_idx = ont_identifier[:-2]
                port = self._model.get_port('name', port_idx)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                ont = self._model.get_ont("name", ont_identifier)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            if case == 'up':
                ont.admin_up()
            elif case == 'down':
                ont.admin_down()

        elif self._validate(args, 'ont', 'sw-ctrl', '2', 'hw-version', 'G2110V1D0*', 'ont-variant', 'DO',
                            'plnd-sw-version', '2.6.0-EFT4', 'plnd-sw-ver-conf', '2.6.0-EFT4', 'sw-dwload-ver',
                            '2.6.0-EFT4'):
            # This function sets a specific software version for a device with a certain serial number.
            # Since we can't really install software on our virtual devices, we just return.
            return

        elif self._validate(args, 'slot', str, 'planned-type', str, 'unlock'):
            identifier, planned_type = self._dissect(args, 'slot', str, 'planned-type', str, 'unlock')

            if ":" in identifier:
                identifier = identifier.split(":")[1]
                try:
                    card = self._model.get_card("name", identifier)
                    card.set_planned_type(planned_type)
                    card.set_admin_state('unlock')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'ont', 'no', 'interface', str):
            ont_idx, = self._dissect(args, 'ont', 'no', 'interface', str)

            try:
                ont = self._model.get_ont('name', ont_idx)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            for ont_port in self._model.ont_ports:
                if ont_port.ont_id == ont.id:
                    for cpe in self._model.cpes:
                        if cpe.ont_port_id == ont_port.id:
                            for cpe_port in self._model.cpe_ports:
                                if cpe_port.cpe_id == cpe.id:
                                    params = dict(connected_type='cpe', connected_id=cpe_port.id)
                                    service_port = self._model.get_service_port_by_values(params)
                                    if service_port is not None:
                                        params = dict(service_port_id=service_port.id,)
                                        service_vlan = self._model.get_service_vlan_by_values(params)
                                        if service_vlan is not None:
                                            service_vlan.delete()
                                        service_port.delete()
                                    cpe_port.delete()
                            cpe.delete()
                    params = dict(connected_type='ont', connected_id=ont_port.id)
                    service_port = self._model.get_service_port_by_values(params)
                    if service_port is not None:
                        params = dict(service_port_id=service_port.id, )
                        service_vlan = self._model.get_service_vlan_by_values(params)
                        if service_vlan is not None:
                            service_vlan.delete()
                        service_port.delete()
                    ont_port.delete()
            ont.delete()

        elif self._validate(args, 'ont', 'interface', str, 'sw-ver-pland', 'auto', 'sernum', str, 'sw-dnload-version',
                            'auto', 'plnd-var', 'DO', 'enable-aes', 'enable'):
            ont_idx, cpe_id_raw = self._dissect(args, 'ont', 'interface', str, 'sw-ver-pland', 'auto', 'sernum', str,
                                                'sw-dnload-version', 'auto', 'plnd-var', 'DO', 'enable-aes', 'enable')

            if cpe_id_raw[4] == ':':
                cpe_st, cpe_en = cpe_id_raw.split(':', maxsplit=1)
                cpe_id = cpe_st + cpe_en
            else:
                cpe_id = cpe_id_raw

            try:
                port_idx = ont_idx[:-2]
                port = self._model.get_port('name', port_idx)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                ont = self._model.get_ont('name', ont_idx)
                assert ont.port_id == port.id
            except (exceptions.SoftboxenError, AssertionError):
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                ont_port = self._model.get_ont_port('ont_id', ont.id)
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            try:
                cpe = self._model.get_cpe('serial_no', cpe_id)
                assert cpe.ont_port_id == ont_port.id
            except (exceptions.SoftboxenError, AssertionError):
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)

        elif self._validate(args, 'ont', 'slot', str, 'planned-card-type', 'ethernet', 'plndnumdataports', '1',
                            'plndnumvoiceports', '0', 'admin-state', str):
            ont_identifier, admin_param = self._dissect(args, 'ont', 'slot', str, 'planned-card-type', 'ethernet',
                                                        'plndnumdataports', '1', 'plndnumvoiceports', '0',
                                                        'admin-state', str)
            ont_idx = ont_identifier[:-2]

            try:
                ont = self._model.get_ont('name', ont_idx)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if admin_param == 'up':
                ont.admin_up()
            elif admin_param == 'down':
                ont.admin_down()
            else:
                raise exceptions.CommandSyntaxError(command=command)

            create_ont_port = True
            for ont_port in self._model.ont_ports:
                if ont_port.ont_id == ont.id:
                    create_ont_port = False
                    break

            if create_ont_port:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_system(self, command, *args, context=None):
        self.process(ConfigureSystemCommandProcessor, 'login', 'mainloop', 'configure', 'system', args=args,
                     return_to=ConfigureCommandProcessor, context=context)

    def do_vlan(self, command, *args, context=None):
        self.process(ConfigureVlanCommandProcessor, 'login', 'mainloop', 'configure',
                     'vlan', args=args, return_to=ConfigureCommandProcessor, context=context)

    def do_service(self, command, *args, context=None):
        self.process(ConfigureServiceCommandProcessor, 'login', 'mainloop', 'configure',
                     'service', args=args, return_to=ConfigureCommandProcessor, context=context)

    def do_xdsl(self, command, *args, context=None):
        if self._validate(args, '?'):
            text = self._render('xdsl_help', context=context)
            self._write(text)
        elif self._validate(args, 'line', '?'):
            text = self._render('line_help', context=context)
            self._write(text)
        elif self._validate(args, 'line', str, '?'):
            text = self._render('port_helpt', context=context)
            self._write(text)
        elif self._validate(args[:2], 'line', str):
            port_identifier, = self._dissect(args, 'line', str)
            port = self._model.get_port("name", port_identifier)
            name_pattern = re.compile("name:([^ ]+)")
            profile_types = ('dpbo', 'service', 'spectrum', 'vect', 'qos')
            configure_profiles = dict()
            admin_up = None
            profile_args = args[2:]
            for i in range(len(profile_args)):
                for profile_type in profile_types:
                    if profile_args[i] == profile_type + "-profile" and profile_args[i - 1] == 'no':
                        configure_profiles[profile_type] = False
                        break
                    if i < len(args) - 1:
                        if profile_args[i] == profile_type + "-profile" and name_pattern.match(profile_args[i + 1]):
                            configure_profiles[profile_type] = name_pattern.search(profile_args[i + 1]).group(1)
                            break
                if profile_args[i] == 'admin-up' and profile_args[i - 1] != 'no':
                    admin_up = True
                elif profile_args[i] == 'admin-up' and profile_args[i - 1] == 'no':
                    admin_up = False

            if admin_up is True:
                port.admin_up()
            elif admin_up is False:
                port.admin_down()

            for profile_type in configure_profiles:
                if configure_profiles[profile_type] is False:
                    port.update_profile(None, profile_type)
                else:
                    try:
                        profile = self._model.get_port_profile("name", configure_profiles[profile_type])
                    except exceptions.SoftboxenError:
                        text = self._render('instance_does_not_exist', context=context)
                        self._write(text)
                        return
                    port.update_profile(profile.id, profile_type)
        elif self._validate(args, 'board', str, 'vect-fallback', 'spectrum-profile', 'name:VDSL_VECT_FALLBACK'):
            card_identifier, = self._dissect(args, 'board', str, 'vect-fallback',
                                             'spectrum-profile', 'name:VDSL_VECT_FALLBACK')

            card = self._model.get_card('name', card_identifier)

            try:
                profile = self._model.get_port_profile('name', 'VDSL_VECT_FALLBACK')
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            card.set_vect_fallback_spectrum_profile(profile.id)
        elif self._validate(args, 'board', str, 'vect-fallback', 'fb-vplt-com-fail', 'fb-cpe-cap-mism',
                            'fb-conf-not-feas'):
            card_identifier, = self._dissect(args, 'board', str, 'vect-fallback', 'fb-vplt-com-fail', 'fb-cpe-cap-mism',
                                             'fb-conf-not-feas')

            card = self._model.get_card('name', card_identifier)
            card.set_vect_fallback_fb_vplt_com_fail(True)
            card.set_vect_fallback_fb_cpe_cap_mism(True)
            card.set_vect_fallback_fb_conf_not_feas(True)
        elif self._validate(args, 'board', 'nt', 'vce-profile', 'name:vce-default'):
            try:
                management_card = self._model.get_card('name', 'nt-a')
            except exceptions.InvalidInputError:
                # try retrieving mgmt-card 'nt-b' -> raises error if not found
                management_card = self._model.get_card('name', 'nt-b')

            try:
                profile = self._model.get_port_profile('name', 'vce-default')
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
                return

            management_card.set_vce_profile(profile.id)
        elif self._validate(args, 'board', str, 'vplt-autodiscover', 'enable'):
            card_identifier, = self._dissect(args, 'board', str, 'vplt-autodiscover', 'enable')
            if card_identifier == 'nt':
                # try retrieving mgmt-card 'nt-a'
                try:
                    card = self._model.get_card('name', 'nt-a')
                except exceptions.InvalidInputError:
                    # try retrieving mgmt-card 'nt-b' -> raises error if not found
                    card = self._model.get_card('name', 'nt-b')
            else:
                card = self._model.get_card('name', card_identifier)

            card.set_vplt_autodiscover('enabled')
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_alarm(self, command, *args, context=None):
        self.process(ConfigureAlarmCommandProcessor, 'login', 'mainloop', 'configure',
                     'alarm', args=args, return_to=ConfigureCommandProcessor, context=context)

    def do_bridge(self, command, *args, context=None):
        self.process(ConfigureBridgeCommandProcessor, 'login', 'mainloop', 'configure',
                     'bridge', args=args, return_to=ConfigureCommandProcessor, context=context)

    def do_ethernet(self, command, *args, context=None):
        if self._validate(args, 'line', str, 'admin-up'):
            port_identifier, = self._dissect(args, 'line', str, 'admin-up')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.CommandSyntaxError(command=command)

            port.admin_up()
        elif self._validate(args, 'line', str, 'no', 'admin-up'):
            port_identifier, = self._dissect(args, 'line', str, 'no', 'admin-up')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.CommandSyntaxError(command=command)

            port.admin_down()
        elif self._validate(args, 'line', str, 'mau', '1', 'power', 'up'):
            port_identifier, = self._dissect(args, 'line', str, 'mau', '1', 'power', 'up')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.CommandSyntaxError(command=command)
            ont = self._model.get_ont("port_id", port.id)

            ont.power_up()
        elif self._validate(args, 'line', str, 'mau', '1', 'power', 'down'):
            port_identifier, = self._dissect(args, 'line', str, 'mau', '1', 'power', 'down')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.CommandSyntaxError(command=command)
            ont = self._model.get_ont("port_id", port.id)

            ont.power_down()
        elif self._validate(args, 'line', str, 'mau', '1', 'type', str):
            port_identifier, type = self._dissect(args, 'line', str, 'mau', '1', 'type', str)
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.InvalidInputError

            mau = self._model.get_ont("port_id", port.id)
            mau.set_type(type)
        elif self._validate(args, 'line', str, 'mau', '1', 'type', str, 'autonegotiate', 'cap1000base-xfd'):
            port_identifier, type = self._dissect(args, 'line', str, 'mau', '1', 'type', str, 'autonegotiate',
                                                  'cap1000base-xfd')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.InvalidInputError

            mau = self._model.get_ont("port_id", port.id)
            mau.set_type(type)
            mau.autonegotiate()
            mau.set_cap1000base_xfd('yes')
        elif self._validate(args, 'line', str, 'port-type', 'uni', 'admin-up'):
            port_identifier, = self._dissect(args, 'line', str, 'port-type', 'uni', 'admin-up')
            port = self._model.get_port("name", port_identifier)
            card = self._model.get_card("id", port.card_id)
            if card.product != 'ftth':
                raise exceptions.InvalidInputError

            port.admin_up()
        elif self._validate(args[:3], 'ont', str, 'cust-info') and self._validate(args[-2:], 'auto-detect', str):
            ont_port_identifier, = self._dissect(args[:3], 'ont', str, 'cust-info')
            customer_info = self.name_joiner(args)
            ont_port_speed, = self._dissect(args[-2:], 'auto-detect', str)

            try:
                ont_port = self._model.get_ont_port('name', ont_port_identifier)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            ont_port.set_description(customer_info)
            ont_port.set_speed(ont_port_speed)

        elif self._validate(args, 'ont', str, 'admin-state', str):
            ont_port_identifier, case = self._dissect(args, 'ont', str, 'admin-state', str)

            try:
                ont_port = self._model.get_ont_port('name', ont_port_identifier)
                ont = self._model.get_ont('id', ont_port.ont_id)
                port = self._model.get_port('id', ont.port_id)
                card = self._model.get_card('id', port.card_id)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if card.product != 'ftth-pon':
                raise exceptions.CommandSyntaxError(command=command)

            if case == 'up':
                ont_port.admin_up()
            elif case == 'down':
                ont_port.admin_down()
            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_software_mngt(self, command, *args, context=None):
        if self._validate(args, 'oswp', '2', 'primary-file-server-id', str):
            primary_file_server_id, = self._dissect(args, 'oswp', '2', 'primary-file-server-id', str)
            try:
                assert primary_file_server_id.count('.') == 3
                for i in primary_file_server_id.split('.'):
                    assert 0 <= int(i) <= 255
                self._model.set_primary_file_server_id(primary_file_server_id)
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)

            self.process(ConfigureSoftwaremngtOswp2CommandProcessor, 'login', 'mainloop', 'configure',
                         'software_mngt', 'oswp', '2', args=(), return_to=ConfigureCommandProcessor,
                         context=context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_linetest(self, command, *args, context=None):
        self.process(ConfigureLinetestCommandProcessor, 'login', 'mainloop', 'configure',
                     'linetest', args=args, return_to=ConfigureCommandProcessor, context=context)

    def do_qos(self, command, *args, context=None):
        self.process(ConfigureQosCommandProcessor, 'login', 'mainloop', 'configure',
                     'qos', args=args, return_to=ConfigureCommandProcessor, context=context)


class ConfigureQosCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_interface(self, command, *args, context=None):
        interface_identifier = args[0]

        try:
            qos_interface = self._model.get_qos_interface('name', interface_identifier)
            context['qos_interface'] = qos_interface

        except exceptions.InvalidInputError:
            self._model.add_qos_interface(name=interface_identifier)

            qos_interface = self._model.get_qos_interface('name', interface_identifier)
            context['qos_interface'] = qos_interface

        self.process(ConfigureQosInterfaceCommandProcessor, 'login', 'mainloop', 'configure',
                     'qos', 'interface', args=args[1:], return_to=ConfigureQosCommandProcessor, context=context)


class ConfigureQosInterfaceCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_us_num_queue(self, command, *args, context=None):
        if self._validate(args, str):
            num, = self._dissect(args, str)
            context['qos_interface'].set('us_num_queue', num)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_upstream_queue(self, command, *args, context=None):
        if self._validate(args, '0', 'priority', '1', 'weight', '1', 'bandwidth-profile', str, 'bandwidth-sharing',
                          'uni-sharing'):
            u_p_raw, = self._dissect(args, '0', 'priority', '1', 'weight', '1', 'bandwidth-profile', str,
                                     'bandwidth-sharing', 'uni-sharing')

            if u_p_raw.startswith('name:'):
                _, upstream_profile = u_p_raw.split(':', maxsplit=1)
            else:
                raise exceptions.CommandSyntaxError(command=command)
            context['qos_interface'].set('upstream_queue_bandwidth_profile', upstream_profile)
            context['qos_interface'].set('upstream_queue_bandwidth_sharing', 'uni-sharing')
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureServiceCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def create_sap(self, vlan_id, port_identifier, command):
        if port_identifier.startswith('nt-a'):
            port_p1, port_p2, port_p3, vlan_id_rep = port_identifier.split(':')
            port_idx = port_p1 + ':' + port_p2 + ':' + port_p3
        elif port_identifier.startswith('lt'):
            port_p1, port_p2, vlan_id_rep = port_identifier.split(':')
            port_idx = port_p1 + ':' + port_p2
        else:
            raise exceptions.CommandSyntaxError(command=command)

        if vlan_id != vlan_id_rep:
            raise exceptions.CommandSyntaxError(command=command)

        if port_idx == 'nt-a:xfp:1':
            try:
                port = self._model.get_port('name', port_idx)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                vlan = self._model.add_vlan(name='Vlan_' + vlan_id, number=int(vlan_id), shutdown=False, tag='tagged')
            self._model.add_service_port(name=port_idx, connected_id=port.id, connected_type='port')
            try:
                service_port = self._model.get_service_port('name', port_idx)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            self._model.add_service_vlan(vlan_id=vlan.id, service_port_id=service_port.id)
            try:
                service_vlan = self._model.get_service_vlan('vlan_id', vlan.id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif re.match("lt:[0-9]/[0-9]/\[1\.\.\.4\]", port_idx):
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                vlan = self._model.add_vlan(name='Vlan_' + vlan_id, number=int(vlan_id), shutdown=False)

            for i in range(1, 5):
                card_name = '1/1/' + str(i)
                card_exists = True
                try:
                    card = self._model.get_card('name', card_name)
                except exceptions.SoftboxenError:
                    card_exists = False

                if card_exists:
                    self._model.add_service_vlan(vlan_id=vlan.id, card_id=card.id, name=card_name)
                try:
                    _ = self._model.get_service_vlan('name', card_name)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

        elif re.match("lt:[0-9]/[0-9]/\[1\.\.\.8\]", port_idx):
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                vlan = self._model.add_vlan(name='Vlan_' + vlan_id, number=int(vlan_id), shutdown=False)

            for i in range(1, 9):
                card_name = '1/1/' + str(i)
                card_exists = True
                try:
                    card = self._model.get_card('name', card_name)
                except exceptions.SoftboxenError:
                    card_exists = False

                if card_exists:
                    self._model.add_service_vlan(vlan_id=vlan.id, card_id=card.id, name=card_name)
                    try:
                        _ = self._model.get_service_vlan('name', card_name)
                    except exceptions.SoftboxenError:
                        raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_vpls(self, command, *args, context=None):
        if self._model.model != '7360':
            raise exceptions.CommandSyntaxError(command=command)

        if self._validate(args[:8], str, 'customer', '2', 'v-vpls', 'vlan', str, 'create', 'description'):
            vlan_id, vlan_id_rep = self._dissect(args[:8], str, 'customer', '2', 'v-vpls', 'vlan', str,
                                                 'create', 'description')
            description = self.name_joiner(args)

            if vlan_id != vlan_id_rep:
                raise exceptions.CommandSyntaxError(command=command)

            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                self._model.add_vlan(number=int(vlan_id), name=description, shutdown=False)

                try:
                    vlan = self._model.get_vlan('number', int(vlan_id))
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
                return
            self._write('\nVlan with this name already exists\n\n')

        elif self._validate(args, str, 'sap', str, 'create', 'no', 'shutdown'):
            vlan_id, port_identifier = self._dissect(args, str, 'sap', str, 'create', 'no', 'shutdown')
            self.create_sap(vlan_id, port_identifier, command)

        elif self._validate(args, str, 'create', 'sap', str, 'no', 'shutdown'):
            vlan_id, port_identifier = self._dissect(args, str, 'create', 'sap', str, 'no', 'shutdown')
            self.create_sap(vlan_id, port_identifier, command)

        elif self._validate(args, str, 'no', 'shutdown'):
            vlan_id, = self._dissect(args, str, 'no', 'shutdown')
            self._model.add_vlan(name='Vlan_' + vlan_id, number=int(vlan_id), shutdown=False)
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanShubCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_dual_tag_mode(self, command, *args, context=None):
        if len(args) == 0:
            try:
                card = self._model.get_card('name', 'nt-a')
            except exceptions.SoftboxenError:
                try:
                    card = self._model.get_card('name', 'nt-b')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            card.set_dual_tag_mode(True)

        else:
            raise exceptions.CommandSyntaxError(command=command)

        return

    def do_id(self, command, *args, context=None):
        if type(args[0]) == str:
            vlan_id = args[0]
            context['vlan_id'] = vlan_id
            self.process(ConfigureVlanShubIdCommandProcessor, 'login', 'mainloop', 'configure', 'vlan',
                         'shub', 'id', args=args[1:], return_to=ConfigureVlanShubCommandProcessor,
                         context=dict(context, vlan_id=vlan_id))
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanShubIdCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_mode(self, command, *args, context=None):
        if self._validate(args, str):
            mode, = self._dissect(args, str)
            try:
                vlan = self._model.get_vlan('number', int(context['vlan_id']))
                vlan.set_mode(mode)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_name(self, command, *args, context=None):
        vlan_name = ''
        for arg in args:
            vlan_name += arg
        try:
            vlan = self._model.get_vlan('number', int(context['vlan_id']))
            vlan.change_name(vlan_name)
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)
        return

    def do_egress_port(self, command, *args, context=None):
        if self._validate(args, str):
            card_idx, = self._dissect(args, str)
            try:
                card = self._model.get_card('position', card_idx)
                vlan = self._model.get_vlan('number', int(context['vlan_id']))
                port = self._model.get_port('card_id', card.id)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            if not vlan.egress_port.__contains__(card_idx):
                egress_port = vlan.egress_port + card_idx + ','
                vlan.set_egress_port(egress_port)
                port.set_egress_port(True)

            self.process(ConfigureVlanShubIdEgressPortCommandProcessor, 'login', 'mainloop', 'configure', 'vlan',
                         'shub', 'id', 'EgressPort', args=(), return_to=ConfigureVlanShubIdCommandProcessor,
                         context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanShubIdEgressPortCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureSoftwaremngtOswp2CommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureInterfacePortCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def set_description(self, args, port):
        if args[0] == "\"\"":
            port.set_description(None)
        else:
            username = self.name_joiner(args)
            port.set_description(username)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_user(self, command, *args, context=None):
        port = self._model.get_port("name", context['port_idx'])
        self.set_description(args, port)

    def do_admin_up(self, command, *args, context=None):
        if len(args) == 0:
            try:
                port_idx = context['port_idx']
                if port_idx.count('/') == 3:
                    port = self._model.get_port('name', port_idx)
                    port.admin_up()
                else:
                    ont_port = self._model.get_ont_port('name', port_idx)
                    ont_port.admin_up()
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args[:1], 'user'):
            try:
                ont_port = self._model.get_ont_port('name', context['port_idx'])

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            ont_port.admin_up()
            self.set_description(args, ont_port)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_admin_up(self, command, *args, context=None):
        if len(args) == 0:
            try:
                port_idx = context['port_idx']
                if port_idx.count('/') == 3:
                    port = self._model.get_port('name', port_idx)
                    port.admin_down()
                else:
                    ont_port = self._model.get_ont_port('name', port_idx)
                    ont_port.admin_down()
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args[:1], 'user'):
            try:
                ont_port = self._model.get_ont_port('name', context['port_idx'])

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            ont_port.admin_down()
            self.set_description(args, ont_port)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_user(self, command, *args, context=None):
        port = self._model.get_port("name", context['port_idx'])
        args = ('""',)
        self.set_description(args, port)


class ConfigureBridgeCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_no_port(self, command, *args, context=None):
        if self._validate(args, str):
            port_identifier, = self._dissect(args, str)

            try:
                service_port = self._model.get_service_port('name', port_identifier)
                service_port.delete()
            except exceptions.SoftboxenError:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)

    def do_port(self, command, *args, context=None):
        port_identifier = args[0]

        try:
            service_port = self._model.get_service_port('name', port_identifier)
        except exceptions.SoftboxenError:
            port_type = None
            port = None

            if re.search('^[0-9]+/[0-9]+/[0-9]+/[0-9]+$', port_identifier):
                port_type = 'port'
                port = self._model.get_port('name', port_identifier)
            elif re.search('^[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+$', port_identifier):
                port_type = 'ont'
                port = self._model.get_ont_port('name', port_identifier)
            elif re.search('^[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+$', port_identifier) or \
                    re.search('^[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+$', port_identifier):
                port_type = 'cpe'
                port = self._model.get_cpe_port('name', port_identifier)

            self._model.add_service_port(name=port_identifier, connected_type=port_type, connected_id=port.id)

            service_port = self._model.get_service_port('name', port_identifier)

        context['service_port'] = service_port

        self.process(ConfigureBridgePortCommandProcessor, 'login', 'mainloop', 'configure', 'bridge', 'port',
                     'port_identifier', args=args[1:], return_to=ConfigureCommandProcessor, context=context)


class ConfigureBridgePortVlanidCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureBridgePortCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def set_qos_profile(self, profile_identifier, port, command, context):
        if 'name:' in profile_identifier:
            profile_name = profile_identifier.split(":")[1]
        else:
            raise exceptions.CommandSyntaxError(command=command)

        try:
            profile = self._model.get_port_profile("name", profile_name)
        except exceptions.SoftboxenError:
            text = self._render('instance_does_not_exist', context=context)
            self._write(text)
            return

        port.set_qos_profile(profile.id)

    def do_max_unicast_mac(self, command, *args, context=None):
        if self._validate(args, str):
            max_unicast_mac, = self._dissect(args, str)
            context['service_port'].set_max_unicast_mac(int(max_unicast_mac))
        elif self._validate(args, '4', 'qos-profile', str):
            context['service_port'].set_max_unicast_mac(4)
            profile_identifier, = self._dissect(args, '4', 'qos-profile', str)
            self.set_qos_profile(profile_identifier, context['service_port'], command, context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pvid(self, command, *args, context=None):
        if self._validate(args, str):
            pvid, = self._dissect(args, str)
            context['service_port'].set_pvid(int(pvid))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_vlan_id(self, command, *args, context=None):
        vlan_id = args[0]

        vlan_scope_local = False
        for i in range(len(args)):
            if i < len(args) - 1:
                if (args[i], args[i + 1]) == ('vlan-scope', 'local'):
                    vlan_scope_local = True

        try:
            vlan = self._model.get_vlan('number', int(vlan_id))
        except exceptions.SoftboxenError:
            raise exceptions.CommandSyntaxError(command=command)

        service_vlan = self._model.get_service_vlan_by_values(
            {'name': vlan_id, 'service_port_id': context['service_port'].id})
        if service_vlan is None:
            if vlan_scope_local:
                self._model.add_service_vlan(name=vlan_id, service_port_id=context['service_port'].id, vlan_id=vlan.id)
            else:
                try:
                    vlan = self._model.get_vlan("number", int(vlan_id))

                except exceptions.SoftboxenError:
                    self._write("\nError : VLAN MGT error 81 : Given L2-forwarder has not been created yet\n\n")
                    return
                s_port = context['service_port']
                self._model.add_service_vlan(name=vlan_id, service_port_id=s_port.id, vlan_id=vlan.id)

            service_vlan = self._model.get_service_vlan_by_values(
                {'name': vlan_id, 'service_port_id': context['service_port'].id})

        if self._validate(args, str):
            return
        elif self._validate(args, '7', 'network-vlan', str, 'vlan-scope', 'local'):
            l2fwder_vlan_id, = self._dissect(args, '7', 'network-vlan', str, 'vlan-scope', 'local')
            service_vlan.set_l2fwder_vlan(int(l2fwder_vlan_id))
        elif self._validate(args, str, 'untagged'):
            vlan_id, = self._dissect(args, str, 'untagged')
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            vlan.set_tag('untagged')
        elif self._validate(args, str, 'tag', 'single-tagged'):
            vlan_id, = self._dissect(args, str, 'tag', 'single-tagged')
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            vlan.set_tag('single-tagged')
        elif self._validate(args, str, 'l2fwdr-vlan', str, 'vlan-scope', 'local', 'tag', 'single-tagged'):
            _, l2fwder_vlan_id = self._dissect(args, str, 'l2fwdr-vlan', str, 'vlan-scope', 'local', 'tag',
                                               'single-tagged')
            service_vlan.set_l2fwder_vlan(int(l2fwder_vlan_id))
        elif self._validate(args, str, 'l2fwdr-vlan', str, 'vlan-scope', 'local', 'single-tagged'):
            _, l2fwder_vlan_id = self._dissect(args, str, 'l2fwdr-vlan', str, 'vlan-scope', 'local', 'single-tagged')
            service_vlan.set_l2fwder_vlan(int(l2fwder_vlan_id))
        elif self._validate(args, str, 'single-tagged'):
            vlan_id, = self._dissect(args, str, 'single-tagged')
            try:
                vlan = self._model.get_vlan('number', int(vlan_id))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
            vlan.set_tag('single-tagged')
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_qos_profile(self, command, *args, context=None):
        if self._validate(args, str):
            profile_identifier, = self._dissect(args, str)
            self.set_qos_profile(profile_identifier, context['service_port'], command, context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_no_pvid(self, command, *args, context=None):
        context['service_port'].set_pvid(None)

    def do_no_vlan_id(self, command, *args, context=None):
        if self._validate(args, str):
            vlan_number, = self._dissect(args, str)
            params = dict(name=vlan_number, service_port_id=context['service_port'].id)
            service_vlan = self._model.get_service_vlan_by_values(params)
            if service_vlan is not None:
                service_vlan.delete()
            else:
                text = self._render('instance_does_not_exist', context=context)
                self._write(text)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureBoardHwIssueCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_severity(self, command, *args, context=None):
        if self._validate(args, 'critical', 'service-affecting', 'reporting', 'logging'):
            self._model.set_board_hw_issue_reporting_logging(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureBoardInitCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_severity(self, command, *args, context=None):
        if self._validate(args, 'critical', 'service-affecting', 'reporting', 'logging'):
            self._model.set_board_init_reporting_logging(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureBoardInstlMissingCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_severity(self, command, *args, context=None):
        if self._validate(args, 'critical', 'service-affecting', 'reporting', 'logging'):
            self._model.set_board_instl_missing_reporting_logging(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureBoardMissingCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_severity(self, command, *args, context=None):
        if self._validate(args, 'critical', 'service-affecting', 'reporting', 'logging'):
            self._model.set_board_missing_reporting_logging(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigurePluginDcBCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_severity(self, command, *args, context=None):
        if self._validate(args, 'major', 'no', 'service-affecting', 'no', 'reporting', 'no', 'logging'):
            self._model.set_plugin_dc_b_severity(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureXdslLineCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def do_line(self, command, *args, context=None):
        return

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_broadcast_frames(self, command, *args, context=None):
        self._model.set_broadcast_frames(True)

    def do_priority_policy(self, command, *args, context=None):
        if self._validate(args, 'port-default'):
            self._model.set_priority_policy_port_default(True)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_id(self, command, *args, context=None):
        if len(args) > 0 and type(args[0]) == str:
            vlan_id = args[0]

            try:
                vlan = self._model.get_vlan("number", int(vlan_id))

            except (exceptions.InvalidInputError, ValueError):
                box = self._model
                box.add_vlan(number=vlan_id, name=vlan_id, role='access', description='')

                vlan = self._model.get_vlan('number', int(vlan_id))

            self.process(ConfigureVlanIdCommandProcessor, 'login', 'mainloop', 'configure',
                         'vlan', 'id', args=args[1:], return_to=ConfigureVlanCommandProcessor,
                         context=dict(context, vlan=vlan))
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_info(self, command, *args, context=None):
        if args == ():
            text = self._render('info_head', context=context)
            for vlan in self._model.vlans:
                text += self._render('info_body', context=dict(context, vlan=vlan))

            text += self._render('info_bottom', context=context)
            self._write(text)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shub(self, command, *args, context=None):
        self.process(ConfigureVlanShubCommandProcessor, 'login', 'mainloop', 'configure', 'vlan',
                     'shub', args=args, return_to=ConfigureVlanCommandProcessor, context=context)


class ConfigureSystemCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def do_syslog(self, command, *args, context=None):
        if self._validate(args, 'destination', str, 'type', str, 'no', 'disable', 'no', 'upload-rotate'):
            logging_server_ip, udp_logging_server_ip = self._dissect(args, 'destination', str, 'type', str, 'no',
                                                                     'disable', 'no', 'upload-rotate')
            try:
                assert udp_logging_server_ip.count(':') == 3
                ip_string = udp_logging_server_ip.split(':')
                assert ip_string[0] == 'udp'
                assert ip_string[2] == '514'
                assert ip_string[3] == 'unlimited'
                udp_logging_server_ip = ip_string[1]
                assert udp_logging_server_ip.count('.') == 3
                for i in udp_logging_server_ip.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            self._model.set_logging_server_ip(logging_server_ip)
            self._model.set_udp_logging_server_ip(udp_logging_server_ip)
            pass
        elif self._validate(args, 'route', str, 'msg-type', 'eqpt', 'facility', 'syslog', 'emergency', 'alert',
                            'critical', 'error', 'warning'):
            route, = self._dissect(args, 'route', str, 'msg-type', 'eqpt', 'facility', 'syslog', 'emergency', 'alert',
                                   'critical', 'error', 'warning')
            self._model.set_syslog_route(route)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_security(self, command, *args, context=None):
        self.process(ConfigureSystemSecuritySubProcessor, 'login', 'mainloop', 'configure', 'system', 'security',
                     args=args,
                     return_to=ConfigureSystemCommandProcessor, context=context)

    def do_port_num_in_proto(self, command, *args, context=None):
        if self._validate(args, str):
            port_num, = self._dissect(args, str)
            try:
                assert port_num == 'type-based' or port_num == 'legacy-num' or port_num == 'position-based'
                self._model.set_port_num_in_proto(port_num)
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_max_lt_link_speed(self, command, *args, context=None):
        if self._validate(args, 'link-speed', 'ten-gb'):
            try:
                self._model.set_max_lt_link_speed('ten-gb')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_contact_person(self, command, *args, context=None):
        contact_person = self.name_joiner(args)
        box = self._model
        box.set_contact_person(contact_person)

    def do_sntp(self, command, *args, context=None):
        self.process(ConfigureSystemSntpCommandProcessor, 'login', 'mainloop', 'configure', 'system', 'sntp',
                     args=args,
                     return_to=ConfigureSystemCommandProcessor, context=context)

    def do_loop_id_syntax(self, command, *args, context=None):
        if self._validate(args[:8], 'atm-based-dsl', str, 'eth', 'Slot/Port"', 'efm-based-dsl', str, 'eth',
                          'Slot/Port"'):
            ip_address, ip_address_rep = self._dissect(args[:8], 'atm-based-dsl', str, 'eth', 'Slot/Port"',
                                                       'efm-based-dsl', str, 'eth', 'Slot/Port"')

            if ip_address != ip_address_rep:
                raise exceptions.CommandSyntaxError(command=command)
            elif not(re.match("\"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip_address)):
                raise exceptions.CommandSyntaxError(command=command)
            elif not(re.match("\"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip_address_rep)):
                raise exceptions.CommandSyntaxError(command=command)

            if self._validate(args[8:], 'efm-based-pon', str, 'eth', 'Slot/Port/ONU/OnuSlt/UNI"'):
                ip_address_sec_rep, = self._dissect(args[8:], 'efm-based-pon', str, 'eth', 'Slot/Port/ONU/OnuSlt/UNI"')
                if ip_address != ip_address_sec_rep:
                    raise exceptions.CommandSyntaxError(command=command)
                elif not (re.match("\"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip_address_sec_rep)):
                    raise exceptions.CommandSyntaxError(command=command)

            self.process(ConfigureSystemLoopidsyntaxSubProcessor, 'login', 'mainloop', 'configure', 'system',
                         'loop_id_syntax', args=(), return_to=ConfigureSystemCommandProcessor, context=context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_id(self, command, *args, context=None):
        if self._validate(args, str, 'name', 'isam', 'location', str):
            isam_id, isam_location = self._dissect(args, str, 'name', 'isam', 'location', str)

            box = self._model
            box.set_isam_id(isam_id)
            box.set_isam_location(isam_location)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_management(self, command, *args, context=None):
        if self._validate(args, 'no', 'default-route'):
            self._model.set_default_route(None)

        elif self._validate(args, 'host-ip-address', str):
            new_ip, = self._dissect(args, 'host-ip-address', str)

            if new_ip.startswith('manual:') and new_ip.endswith('/24'):
                try:
                    _, ip_half_ready = new_ip.split(':')
                    ip, _ = ip_half_ready.split('/')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

                if re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", ip):
                    self._model.set_mgmt_address(ip)
                else:
                    raise exceptions.CommandSyntaxError(command=command)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'default-route', str):
            gateway, = self._dissect(args, 'default-route', str)

            if re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", gateway):
                self._model.set_default_route(gateway)

            else:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_mgnt_vlan_id(self, command, *args, context=None):
        if self._validate(args, str):
            mngt_vlan_id, = self._dissect(args, str)

            self._model.add_vlan(number=int(mngt_vlan_id), name='Mgnt-Vlan')

            try:
                _ = self._model.get_vlan('number', int(mngt_vlan_id))

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shub(self, command, *args, context=None):
        if self._validate(args, 'entry', 'vlan', 'ext-vlan-id', str):
            vlan_id, = self._dissect(args, 'entry', 'vlan', 'ext-vlan-id', str)
            try:
                card = self._model.get_card('name', 'nt-a')
            except exceptions.SoftboxenError:
                try:
                    card = self._model.get_card('name', 'nt-b')
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)

            card.set_entry_vlan_number(vlan_id)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemLoopidsyntaxSubProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemSntpCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_server_table(self, command, *args, context=None):
        if self._validate(args, 'ip-address', str):
            ip_address, = self._dissect(args, 'ip-address', str)
            try:
                assert ip_address.count('.') == 3
                for i in ip_address.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)

            if self._model.sntp_server_table == '':
                self._model.set_sntp_server_table(ip_address)
            else:
                ip = self._model.sntp_server_table + ', ' + ip_address
                self._model.set_sntp_server_table(ip)

            context['ip_address'] = ip_address
            self.process(ConfigureSystemSntpServertableIPSubProcessor, 'login', 'mainloop', 'configure', 'system',
                         'sntp', 'server_table', 'ip_address', 'ip', args=(),
                         return_to=ConfigureSystemCommandProcessor, context=context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_server_ip_addr(self, command, *args, context=None):
        if len(args) == 1:
            ip = args[0]
            try:
                assert ip.count('.') == 3
                for i in ip.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
            self._model.set_sntp_server_ip_address(ip)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_enable(self, command, *args, context=None):
        if self._validate(args, 'timezone-offset', str):
            offset, = self._dissect(args, 'timezone-offset', str)
            try:
                assert -12 <= int(offset) <= 14
                self._model.set_timezone_offset(offset)
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemSntpServertableIPSubProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemSecuritySubProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_login_banner(self, command, *args, context=None):
        pattern = re.compile(".+\"(.+)\"")
        banner, = pattern.match(context['raw_line']).groups(1)
        banner = banner.replace("\\r\\n", "\r\n").replace("\\\\\\", "\\").replace("\\\\", "\\")

        self._model.set_login_banner(banner)

    def do_welcome_banner(self, command, *args, context=None):
        pattern = re.compile(".+\"(.+)\"")
        banner, = pattern.match(context['raw_line']).groups(1)
        banner = banner.replace("\\r\\n", "\r\n").replace("\\\\\\", "\\").replace("\\\\", "\\")

        self._model.set_welcome_banner(banner)

    def do_profile(self, command, *args, context=None):
        if self._validate(args, 'admin', 'slot-numbering', 'type-based'):
            self.process(ConfigureSystemSecurityProfileAdminSubProcessor, 'login', 'mainloop', 'configure', 'system',
                         'security', 'profile', 'admin', args=args, return_to=ConfigureSystemSecuritySubProcessor,
                         context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_operator(self, command, *args, context=None):
        if self._validate(args, str, 'prompt', str):
            username, prompt = self._dissect(args, str, 'prompt', str)
            for creds in self._model.credentials:
                if username != creds.username:
                    raise exceptions.CommandSyntaxError(command=command)

            if prompt.endswith('%d%c'):
                prompt = prompt[:-4]

            box = self._model
            box.set_hostname(prompt)
            self._model.hostname = prompt

            self.process(ConfigureSystemSecurityOperatorCommandProcessor, 'login', 'mainloop', 'configure', 'system',
                         'security', 'operator', 'user_name', args=(), return_to=ConfigureSystemSecuritySubProcessor,
                         context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_snmp(self, command, *args, context=None):
        if self._validate(args, 'community', 'public', 'host-address', str):
            snmp_ip, = self._dissect(args, 'community', 'public', 'host-address', str)
            try:
                snmp, _ = snmp_ip.split('/')
            except ValueError:
                snmp = snmp_ip
            try:
                assert snmp.count('.') == 3
                for i in snmp.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
            self._model.set_public_host_address(snmp)
        elif self._validate(args, 'community', 'futurama', 'host-address', str, 'context', 'ihub'):
            snmp_ip, = self._dissect(args, 'community', 'futurama', 'host-address', str, 'context', 'ihub')
            try:
                snmp, _ = snmp_ip.split('/')
            except ValueError:
                snmp = snmp_ip
            try:
                assert snmp.count('.') == 3
                for i in snmp.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
            self._model.set_futurama_host_address(snmp)
        elif self._validate(args, 'community', 'tellme', 'host-address', str):
            snmp_ip, = self._dissect(args, 'community', 'tellme', 'host-address', str)
            try:
                snmp, _ = snmp_ip.split('/')
            except ValueError:
                snmp = snmp_ip
            try:
                assert snmp.count('.') == 3
                for i in snmp.split('.'):
                    assert 0 <= int(i) <= 255
            except (AssertionError, ValueError):
                raise exceptions.CommandSyntaxError(command=command)
            self._model.set_tellme_host_address(snmp)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemSecurityOperatorCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureSystemSecurityProfileAdminSubProcessor(BaseCommandProcessor, BaseMixIn):

    def do_admin(self, command, *args, context=None):
        if self._validate(args, 'slot-numbering', 'type-based'):
            try:
                self._model.set_admin_slot_numbering('type-based')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanIdCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_name(self, command, *args, context=None):
        if self._validate(args, str):
            vlan_name, = self._dissect(args, str)
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                vlan.change_name(vlan_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        elif len(args) >= 2:
            vlan_name = self.name_joiner(args)

            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                vlan.change_name(vlan_name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_mode(self, command, *args, context=None):
        if self._validate(args, str):
            vlan_mode, = self._dissect(args, str)
            try:
                vlan = self._model.get_vlan('number', context['vlan'].number)
                vlan.set_mode(vlan_mode)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_protocol_filter(self, command, *args, context=None):
        if self._validate(args, 'pass-pppoe'):
            context['vlan'].set_protocol_filter('pass-pppoe')
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_in_qos_prof_name(self, command, *args, context=None):
        if self._validate(args, str):
            name, = self._dissect(args, str)
            context['vlan'].set_in_qos_prof_name(name)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_new_broadcast(self, command, *args, context=None):
        if self._validate(args, 'enable'):
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_new_broadcast('enable')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_new_secure_fwd(self, command, *args, context=None):
        if self._validate(args, 'enable'):
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_new_secure_fwd('enable')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_aging_time(self, command, *args, context=None):
        if self._validate(args, str):
            time, = self._dissect(args, str)
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_aging_time(time)
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_circuit_id_dhcp(self, command, *args, context=None):
        if self._validate(args, 'physical-id'):
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_circuit_id_dhcp('physical-id')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_remote_id_dhcp(self, command, *args, context=None):
        if self._validate(args, 'customer-id'):
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_remote_id_dhcp('customer-id')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_dhcp_opt_82(self, command, *args, context=None):
        if len(args) == 0:
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_dhcp_opt82('enable')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_pppoe_relay_tag(self, command, *args, context=None):
        if self._validate(args, 'true'):
            vlanid = context['vlan'].number
            try:
                vlan = self._model.get_vlan('number', vlanid)
                vlan.set_pppoe_relay_tag('true')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

        elif self._validate(args, 'configurable', 'pppoe-linerate', 'addactuallinerate', 'circuit-id-pppoe',
                            'physical-id', 'remote-id-pppoe', 'customer-id'):
            vlanid = context['vlan'].number
            try:
                vlan = self._model.get_vlan('number', vlanid)
                vlan.set_pppoe_relay_tag('configurable')
                vlan.set_pppoe_linerate('addactuallinerate')
                vlan.set_circuit_id_pppoe('physical-id')
                vlan.set_remote_id_pppoe('customer-id')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_dhcp_opt82_ext(self, command, *args, context=None):
        if self._validate(args, 'enable'):
            try:
                vlan = self._model.vlans.find_by_field_value('number', context['vlan'].number)
                assert vlan.name == 'CPE Management'
                vlan.set_dhcp_opt82_ext('enable')
            except (exceptions.SoftboxenError, AssertionError):
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_shub(self, command, *args, context=None):
        if args == ():
            self.process(ConfigureVlanIdShubCommandProcessor, 'login', 'mainloop', 'configure', 'vlan', 'id', 'shub',
                         args=args, return_to=ConfigureVlanCommandProcessor, context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureVlanIdShubCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_dual_tag_mode(self, command, *args, context=None):
        if args == ():
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_id(self, command, *args, context=None):
        if self._validate(args, str, 'mode', str):
            vlan_idx, mode = self._dissect(args, str, 'mode', str)

            try:
                vlan = self._model.get_vlan('number', int(vlan_idx))
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            vlan.set_mode(mode)
            context['shub_vlan'] = vlan

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_name(self, command, *args, context=None):
        if args[0].startswith('"') and args[-1].endswith('"'):
            name = self.name_joiner(args)
            vlan = context['shub_vlan']
            vlan.change_name(name)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_egress_port(self, command, *args, context=None):
        if self._validate(args, str):
            identifier, = self._dissect(args, str)
            vlan = context['vlan']

            if re.match("lt:1/1/[0-9]+", identifier):
                try:
                    card = self._model.get_card('position', identifier)
                except exceptions.SoftboxenError:
                    text = self._render('instance_does_not_exist', context=context)
                    self._write(text)
                    return

                for port in self._model.ports:
                    if port.card_id == card.id:
                        port.set_egress_port(True)
                        vlan.set_egress_port(port.name)
                        break

            elif identifier == 'nt:sfp:1' or identifier == 'network:0':
                try:
                    card = self._model.get_card('name', 'nt-a')
                except exceptions.SoftboxenError:
                    try:
                        card = self._model.get_card('name', 'nt-b')
                    except exceptions.SoftboxenError:
                        text = self._render('instance_does_not_exist', context=context)
                        self._write(text)
                        return

                for port in self._model.ports:
                    if port.card_id == card.id:
                        port.set_egress_port(True)
                        vlan.set_egress_port(port.name)
                        break

            else:
                raise exceptions.CommandSyntaxError(command=command)


class ConfigureAlarmCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def do_entry(self, command, *args, context=None):
        if args[0] == 'board-hw-issue':
            self.process(ConfigureBoardHwIssueCommandProcessor, 'login', 'mainloop', 'configure', 'alarm', 'entry',
                         'board-hw-issue', args=args[1:], return_to=ConfigureAlarmCommandProcessor, context=context)
        elif args[0] == 'board-init':
            self.process(ConfigureBoardInitCommandProcessor, 'login', 'mainloop', 'configure', 'alarm', 'entry',
                         'board-init', args=args[1:], return_to=ConfigureAlarmCommandProcessor, context=context)
        elif args[0] == 'board-instl-missing':
            self.process(ConfigureBoardInstlMissingCommandProcessor, 'login', 'mainloop', 'configure', 'alarm', 'entry',
                         'board-instl-missing', args=args[1:], return_to=ConfigureAlarmCommandProcessor,
                         context=context)
        elif args[0] == 'board-missing':
            self.process(ConfigureBoardMissingCommandProcessor, 'login', 'mainloop', 'configure', 'alarm', 'entry',
                         'board-missing', args=args[1:], return_to=ConfigureAlarmCommandProcessor, context=context)
        elif args[0] == 'plugin-dc-b':
            self.process(ConfigurePluginDcBCommandProcessor, 'login', 'mainloop', 'configure', 'alarm', 'entry',
                         'plugin-dc-b', args=args[1:], return_to=ConfigureAlarmCommandProcessor, context=context)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)


class ConfigureLinetestCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_single(self, command, *args, context=None):
        self.process(ConfigureLinetestSingleCommandProcessor, 'login', 'mainloop', 'configure',
                     'linetest', 'single', args=args, return_to=ConfigureLinetestCommandProcessor, context=context)


class ConfigureLinetestSingleCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_ltsession(self, command, *args, context=None):
        if self._validate(args[:2], str, 'session-cmd'):
            session_id, = self._dissect(args[:2], str, 'session-cmd')
            context['session_id'] = session_id

            self.process(ConfigureLinetestSingleLtSessionSessionIdCommandProcessor, 'login', 'mainloop', 'configure',
                         'linetest', 'single', 'ltsession', 'session_id', args=args[1:],
                         return_to=ConfigureLinetestSingleCommandProcessor, context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_ltline(self, command, *args, context=None):
        if self._validate(args, str, 'lineid', str, 'line-status', 'intest'):
            session_id, port_identifier = self._dissect(args, str, 'lineid', str, 'line-status', 'intest')

            port_idx = port_identifier[2:]

            try:
                _ = self._model.get_port('name', port_idx)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)

            context['session_id'] = session_id
            context['port_identifier'] = port_identifier

            self.process(ConfigureLinetestSingleLtLineSessionIdLineidPortidentifierCommandProcessor, 'login',
                         'mainloop', 'configure', 'linetest', 'single', 'ltsession', 'session_id', args=args[3:],
                         return_to=ConfigureLinetestSingleCommandProcessor, context=context)

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureLinetestSingleLtSessionSessionIdCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_session_cmd(self, command, *args, context=None):
        if self._validate(args, 'destroy'):
            context['meltStart'] = False
            return

        elif self._validate(args, 'create', 'ownerid', '1', 'timeout-period', '6000', 'line-num', '1', 'type-high',
                            'group', 'type-low', 'none', 'test-parm-num', '0', 'test-mode', 'single'):
            return

        elif self._validate(args, 'starttest'):
            context['meltStart'] = True
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)


class ConfigureLinetestSingleLtLineSessionIdLineidPortidentifierCommandProcessor(BaseCommandProcessor, BaseMixIn):

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_line_status(self, command, *args, context=None):
        if self._validate(args, 'intest'):
            return

        else:
            raise exceptions.CommandSyntaxError(command=command)
