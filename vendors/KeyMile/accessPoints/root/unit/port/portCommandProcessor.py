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
import time


class PortCommandProcessor(BaseCommandProcessor):
    __name__ = 'port'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .portManagementFunctions import main
    from .portManagementFunctions import cfgm
    from .portManagementFunctions import fm
    from .portManagementFunctions import pm
    from .portManagementFunctions import status

    def get_property(self, command, *args, context=None):
        port = self.get_port_component()
        card = self._model.get_card('name', self._parent.component_id)
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc

        elif self._validate(args, 'Portprofile') and context['path'].split('/')[-1] == 'cfgm' and 'SUVM'\
                not in card.board_name and 'SUVD2' not in card.board_name and self.__name__ == 'port':
            context['spacer1'] = self.create_spacers((67,), (port.profile1_name,))[0] * ' '
            context['profile_name'] = port.profile1_name
            text = self._render('port_profile', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'Portprofiles') and context['path'].split('/')[-1] == 'cfgm' and \
                'SUVD2' in card.board_name and self.__name__ == 'port':
            context['spacer1'] = self.create_spacers((67,), (port.profile1_name,))[0] * ' '
            context['profile_name'] = port.profile1_name
            text = self._render('port_profile', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'Portprofiles') and self.__name__ == 'port' and \
                context['path'].split('/')[-1] == 'cfgm' and 'SUVM' in card.board_name:
            context['spacer1'] = self.create_spacers((67,), (port.profile1_enable,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (port.profile1_name,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (port.profile1_elength,))[0] * ' '
            context['spacer4'] = self.create_spacers((67,), (port.profile2_enable,))[0] * ' '
            context['spacer5'] = self.create_spacers((67,), (port.profile2_name,))[0] * ' '
            context['spacer6'] = self.create_spacers((67,), (port.profile2_elength,))[0] * ' '
            context['spacer7'] = self.create_spacers((67,), (port.profile3_enable,))[0] * ' '
            context['spacer8'] = self.create_spacers((67,), (port.profile3_name,))[0] * ' '
            context['spacer9'] = self.create_spacers((67,), (port.profile3_elength,))[0] * ' '
            context['spacer10'] = self.create_spacers((67,), (port.profile4_enable,))[0] * ' '
            context['spacer11'] = self.create_spacers((67,), (port.profile4_name,))[0] * ' '
            context['spacer12'] = self.create_spacers((67,), (port.profile_mode,))[0] * ' '
            text = self._render('port_profiles', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate((args[0],), 'AttainableRate') and context['path'].split('/')[-1] == 'status':
            text = self._render('attainable_rate', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'QuickLoopbackTest') and context['path'].split('/')[-1] == 'status'\
                and (card.product == 'isdn' or 'SUI' in card.board_name) and self.__name__ == 'port':
            context['spacer1'] = self.create_spacers((67,), (port.loopbacktest_state,))[0] * ' '
            context['loopbacktest_state'] = port.loopbacktest_state
            text = self._render('quickloopbacktest', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'LineTestResults') and context['path'].split('/')[-1] == 'status'\
                and 'SUP' in card.board_name and self.__name__ == 'port':
            context['spacer1'] = self.create_spacers((67,), (port.linetest_state,))[0] * ' '
            context['test_state'] = port.linetest_state
            text = self._render('line_results', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'MeltResults') and context['path'].split('/')[-1] == 'status'\
                and card.product != 'isdn' and self.__name__ == 'port':
            context['spacer1'] = self.create_spacers((67,), (port.melttest_state,))[0] * ' '
            context['test_state'] = port.melttest_state
            text = self._render('melt_results', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'AdministrativeStatus') and context['path'].split('/')[-1] == 'main':
            self.map_states(port, 'port')
            context['spacer'] = self.create_spacers((67,), (port.admin_state,))[0] * ' '
            text = self._render('administrative_status', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate(args, 'Labels') and context['path'].split('/')[-1] == 'main':
            context['spacer1'] = self.create_spacers((67,), (port.label1,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (port.label2,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (port.description,))[0] * ' '
            text = self._render('labels', *scopes, context=dict(context, port=port))
            self._write(text)
        elif self._validate((args[0],), 'OperationalStatus') and context['path'].split('/')[-1] == 'main':
            self.map_states(port, 'port')
            port_operational_state = port.operational_state
            context['port_operational_state'] = port_operational_state
            context['spacer'] = self.create_spacers((67,), (port_operational_state,))[0] * ' '
            text = self._render('operational_status', *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        self.access_points = ()
        port = self._model.get_port('name', self._parent.component_id + '/' + self.component_id)

        for chan in self._model.get_chans('port_id', port.id):
            identifier = 'chan-' + chan.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

        for interface in self._model.get_interfaces('port_id', port.id):
            identifier = 'interface-' + interface.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def do_lock(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if len(args) == 0 and context['path'].split('/')[-1] == 'status' and card.product == 'isdn' \
                and self.__name__ == 'port':
            try:
                port = self.get_port_component()
                port.lock_admin()
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_startquickloopbacktest(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if len(args) == 0 and context['path'].split('/')[-1] == 'status' and card.product == 'isdn' \
                and self.__name__ == 'port':
            try:
                port = self.get_port_component()
                port.set_test_state('Running')
                time.sleep(5)
                port.set_test_state('Passed')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_startlinetest(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if len(args) == 0 and context['path'].split('/')[-1] == 'status' and 'SUP' in card.board_name \
                and self.__name__ == 'port':
            try:
                port = self.get_port_component()
                port.set_test_state('Running')
                time.sleep(5)
                port.set_linetest_state('Passed')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_startmeltmeasurement(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if len(args) == 0 and context['path'].split('/')[-1] == 'status' and card.product != 'isdn' \
                and self.__name__ == 'port':
            try:
                port = self.get_port_component()
                port.set_melttest_state('Running')
                time.sleep(5)
                port.set_melttest_state('Passed')
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_unlock(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if len(args) == 0 and context['path'].split('/')[-1] == 'status' and card.product == 'isdn' \
                and self.__name__ == 'port':
            try:
                port = self.get_port_component()
                port.unlock_admin()
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_deleteinterface(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent.component_id)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and card.product == 'ftth':
            # all or interface_id
            name, = self._dissect(args, str)
            if name == 'all':
                port = self.get_port_component()
                for interface in self._model.get_interfaces('port_id', port.id):
                    interface.delete()
            elif name.startswith('interface-'):
                id = name.split('-')[1]
                try:
                    interface = self._model.get_interface('name', self._parent.component_id + '/' + self.component_id + '/' + id)
                    interface.delete()
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_createinterface(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name',  self._parent.component_id)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and 'SUE' in card.board_name:
            # vcc profile and vlan profile
            vlan_prof, = self._dissect(args, str)
            # TODO: Check if profiles := default or profile names
            try:
                port = self.get_port_component()
                id = 1
                for interface in self._model.get_interfaces('port_id', port.id):
                    if interface.port_id is not None:
                        new_id = int(interface.name[-1]) + 1
                        id = new_id if new_id > id else id
                try:
                    name = self._parent.component_id + '/' + self.component_id + '/' + str(id)
                    _ = self._model.get_interface('name',  name)
                    assert False
                except exceptions.SoftboxenError as exe:
                    interf = self._model.add_interface(name=name, port_id=port.id, vlan_profile=vlan_prof)
                    context['spacer1'] = self.create_spacers((57,), (str(id),))[0] * ' '
                    context['id'] = str(id)
                    # TODO: unknown Template
                    text = self._render('interface_success', *scopes, context=context)
                    self._write(text)
                except AssertionError:
                    raise exceptions.CommandSyntaxError(command=command)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_port_component(self):
        return self._model.get_port('name', self._parent.component_id + '/' + self.component_id)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name', self._parent.component_id)
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'Portprofile', str) and context['path'].split('/')[-1] == 'cfgm' and 'SUVM'\
                not in card.board_name and 'SUVD2' not in card.board_name and self.__name__ == 'port':
            profile, = self._dissect(args, 'Portprofile', str)
            try:
                port = self.get_port_component()
                port.set_profile(profile)

            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'Portprofiles', str) and context['path'].split('/')[-1] == 'cfgm' and \
                'SUVD2' in card.board_name and self.__name__ == 'port':
            profile, = self._dissect(args, 'Portprofiles', str)
            try:
                port = self.get_port_component()
                port.set_profile(profile)

            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'Portprofiles', str, str, str, str, str, str, str, str, str, str, str, str) and \
                context['path'].split('/')[-1] == 'cfgm' and 'SUVM' in card.board_name and self.__name__ == 'port':
            en1, name1, elen1, en2, name2, elen2, en3, name3, elen3, en4, name4, mode = self._dissect(args,
                                        'Portprofiles', str, str, str, str, str, str, str, str, str, str, str, str)
            try:
                port = self.get_port_component()
                en1 = True if en1.lower() == 'true' else False
                en2 = True if en2.lower() == 'true' else False
                en3 = True if en3.lower() == 'true' else False
                en4 = True if en4.lower() == 'true' else False
                port.set_profiles(en1, name1, int(elen1), en2, name2, int(elen2), en3, name3, int(elen3), en4, name4, mode)

            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'AdministrativeStatus', str) and context['path'].split('/')[-1] == 'main':
            state, = self._dissect(args, 'AdministrativeStatus', str)
            try:
                port = self.get_port_component()
                if state == 'up':
                    port.admin_up()
                elif state == 'down':
                    port.admin_down()
                else:
                    raise exceptions.SoftboxenError()
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        elif self._validate(args, 'Labels', str, str, str) and context['path'].split('/')[-1] == 'main':
            label1, label2, description = self._dissect(args, 'Labels', str, str, str)
            try:
                port = self.get_port_component()
                port.set_label(label1, label2, description)
            except exceptions.SoftboxenError():
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
        else:
            raise exceptions.CommandSyntaxError(command=command)
