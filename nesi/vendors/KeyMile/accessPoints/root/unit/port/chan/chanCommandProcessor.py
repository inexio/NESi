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


class ChanCommandProcessor(BaseCommandProcessor):
    __name__ = 'chan'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .chanManagementFunctions import main
    from .chanManagementFunctions import cfgm
    from .chanManagementFunctions import fm
    from .chanManagementFunctions import pm
    from .chanManagementFunctions import status

    def _init_access_points(self, context=None):
        self.access_points = ()
        chan = self.get_component()
        card = self._model.get_card('name', self.component_name.split('/')[0])

        for interface in self._model.get_interfaces('chan_id', chan.id):
            if interface.chan_id is not None:
                if card.product != 'adsl':
                    ap_name = 'interface-'
                else:
                    ap_name = 'vcc-'
                identifier = ap_name + interface.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)

    def do_deletevcc(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent._parent.component_name)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and card.product == 'adsl':
            # all or vcc_id
            name, = self._dissect(args, str)
            if name == 'all':
                chan = self.get_component()
                for vcc in self._model.get_interfaces('chan_id', chan.id):
                    vcc.delete()
            elif name.startswith('vcc-'):
                id = name.split('-')[1]
                try:
                    vcc = self._model.get_interface('name', self.component_name + '/' + id)
                    vcc.delete()
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_deleteinterface(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent._parent.component_name)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and card.product != 'adsl' and card.product != 'sdsl':
            # all or interface_id
            name, = self._dissect(args, str)
            if name == 'all':
                chan = self.get_component()
                for interface in self._model.get_interfaces('chan_id', chan.id):
                    interface.delete()
            elif name.startswith('interface-'):
                id = name.split('-')[1]
                try:
                    interface = self._model.get_interface('name', self.component_name + '/' + id)
                    interface.delete()
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_createinterface(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name', self._parent._parent.component_name)
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm' and 'SUV' in card.board_name:
            # vcc profile and vlan profile
            vlan_prof, = self._dissect(args, str)
            # TODO: Check if profiles := default or profile names
            try:
                chan = self.get_component()
                id = 1
                for interface in self._model.get_interfaces('chan_id', chan.id):
                    if interface.chan_id is not None:
                        new_id = int(interface.name[-1]) + 1
                        id = new_id if new_id > id else id
                try:
                    name = self.component_name + '/' + str(id)
                    self._model.get_interface('name', name)
                    assert False
                except exceptions.SoftboxenError as exe:
                    interf = self._model.add_interface(chan_id=chan.id, vlan_profile=vlan_prof)
                    context['spacer1'] = self.create_spacers((57,), (str(id),))[0] * ' '
                    context['id'] = str(id)
                    # TODO: Template is unknown
                    text = self._render('interface_success', *scopes, context=context)
                    self._write(text)
                except AssertionError:
                    raise exceptions.CommandSyntaxError(command=command)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args, str, str) and context['path'].split('/')[-1] == 'cfgm':
            # vcc profile and vlan profile
            vlan_prof, vcc_prof = self._dissect(args, str, str)
            # TODO: Check if profiles := default or profile names
            try:
                chan = self.get_component()
                id = 1
                for interface in self._model.get_interfaces('chan_id', chan.id):
                    if interface.chan_id is not None:
                        new_id = int(interface.name[-1]) + 1
                        id = new_id if new_id > id else id
                try:
                    name = self.component_name + '/' + str(id)
                    self._model.get_interface('name',  name)
                    assert False
                except exceptions.SoftboxenError as exe:
                    interf = self._model.add_interface(chan_id=chan.id, vlan_profile=vlan_prof,
                                                       vcc_profile=vcc_prof)
                    context['spacer1'] = self.create_spacers((57,), (str(id),))[0] * ' '
                    context['id'] = str(id)
                    # TODO: Template is unknown
                    text = self._render('interface_success', *scopes, context=context)
                    self._write(text)
                except AssertionError:
                    raise exceptions.CommandSyntaxError(command=command)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_createvcc(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        card = self._model.get_card('name', self._parent._parent.component_name)
        if self._validate(args, str, str) and context['path'].split('/')[-1] == 'cfgm' and card.product == 'adsl':
            # vcc profile and vlan profile
            vcc_prof, vlan_prof = self._dissect(args, str, str)
            # TODO: Check if profiles := default or profile names
            try:
                chan = self.get_component()
                id = 1
                for vcc in self._model.get_interfaces('chan_id', chan.id):
                    if vcc.chan_id is not None:
                        new_id = int(vcc.name[-1]) + 1
                        id = new_id if new_id > id else id
                try:
                    name = self.component_name + '/' + str(id)
                    self._model.get_interface('name',  name)
                    assert False
                except exceptions.SoftboxenError as exe:
                    vcc = self._model.add_interface(chan_id=chan.id, vcc_profile=vcc_prof,
                                                    vlan_profile=vlan_prof)
                    context['spacer1'] = self.create_spacers((63,), (str(id),))[0] * ' '
                    context['id'] = str(id)
                    # TODO: unknown Template
                    text = self._render('vcc_success', *scopes, context=context)
                    self._write(text)
                except AssertionError:
                    raise exceptions.CommandSyntaxError(command=command)

            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent._parent.component_name)
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'chanprofile', str) and 'SUV' in card.board_name:
            name, = self._dissect(args, 'chanprofile', str)
            try:
                #TODO: Check if profile with this name exists or default
                channel = self.get_component()
                channel.set_profile_name(name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        elif self._validate(args, 'ProfileName', str) and 'SUV' not in card.board_name:
            name, = self._dissect(args, 'ProfileName', str)
            try:
                # TODO: Check if profile with this name exists or default
                channel = self.get_component()
                channel.set_profile_name(name)
            except exceptions.SoftboxenError:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_component(self):
        return self._model.get_chan('name', self.component_name)

    def get_property(self, command, *args, context=None):
        card = self._model.get_card('name', self._parent._parent.component_name)
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'Chanprofile') and 'SUV' in card.board_name:
            channel = self.get_component()
            context['spacer1'] = self.create_spacers((67,), (channel.chan_profile_name,))[0] * ' '
            context['profile_name'] = channel.chan_profile_name
            text = self._render('chan_profile', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'ProfileName') and 'SUV' not in card.board_name:
            channel = self.get_component()
            context['spacer1'] = self.create_spacers((67,), (channel.chan_profile_name,))[0] * ' '
            context['profile_name'] = channel.chan_profile_name
            text = self._render('chan_profile', *scopes, context=context)
            self._write(text)
        elif self._validate(args, 'Status') and context['path'].split('/')[-1] == 'status':
            channel = self.get_component()
            context['spacer1'] = self.create_spacers((67,), (channel.curr_rate_d,))[0] * ' '
            context['spacer2'] = self.create_spacers((67,), (channel.prev_rate_d,))[0] * ' '
            context['spacer3'] = self.create_spacers((67,), (channel.curr_delay_d,))[0] * ' '
            context['spacer4'] = self.create_spacers((67,), (channel.curr_rate_u,))[0] * ' '
            context['spacer5'] = self.create_spacers((67,), (channel.prev_rate_u,))[0] * ' '
            context['spacer6'] = self.create_spacers((67,), (channel.curr_delay_u,))[0] * ' '
            text = self._render('status', *scopes, context=dict(context, channel=channel))
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))
