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
from vendors.KeyMile.accessPoints.root.unit.port.portCommandProcessor import PortCommandProcessor


class PortgroupportCommandProcessor(PortCommandProcessor):
    __name__ = 'portgroupport'
    management_functions = ('main', 'cfgm', 'status')
    access_points = ()

    from .portgroupportManagementFunctions import main
    from .portgroupportManagementFunctions import cfgm
    from .portgroupportManagementFunctions import status

    def get_component(self):
        return self._model.get_portgroupport('name', self.component_name)

    def get_property(self, command, *args, context=None):
        port = self.get_component()
        scopes = ('login', 'base', 'get')
        try:
            super().get_property(command, *args, context=context)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'SubscriberList') and context['path'].split('/')[-1] == 'status' and \
                    self._model.get_card('name', self._parent._parent.component_name).product == 'isdn':
                text = self._render('subscriberList_top', *scopes, context=context)
                i = 0
                for subscriber in self._model.subscribers:
                    if subscriber.type == 'port' and subscriber.address == self.component_name:

                        context['i'] = i
                        context['spacer1'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                        context['spacer2'] = self.create_spacers((63,), (subscriber.registration_state,))[0] * ' '
                        i += 1
                        text += self._render('subscriberList_item2', *scopes,
                                             context=dict(context, subscriber=subscriber))
                text += self._render('subscriberList_bottom', *scopes, context=context)

                self._write(text)
            elif self._validate((args[0],), 'Isdnport') and context['path'].split('/')[-1] == 'cfgm' and \
                port.type == 'ISDN':
                context['spacer1'] = self.create_spacers((67,), (port.enable,))[0] * ' '
                context['spacer2'] = self.create_spacers((67,), (port.register_as_global,))[0] * ' '
                context['spacer3'] = self.create_spacers((67,), (port.register_default_number_only,))[0] * ' '
                context['spacer4'] = self.create_spacers((67,), (port.sip_profile,))[0] * ' '
                context['spacer5'] = self.create_spacers((67,), (port.proxy_registrar_profile,))[0] * ' '
                context['spacer6'] = self.create_spacers((67,), (port.codec_sdp_profile,))[0] * ' '
                context['spacer7'] = self.create_spacers((67,), (port.isdnba_profile,))[0] * ' '
                context['spacer8'] = self.create_spacers((67,), (port.layer_1_permanently_activated,))[0] * ' '
                text = self._render('isdnport_top', *scopes, context=dict(context, port=port))

                i = 0
                for subscriber in self._model.subscribers:
                    if subscriber.type == 'port' and subscriber.address == self.component_name:
                        context['i'] = i
                        context['spacer10'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                        context['spacer11'] = self.create_spacers((63,), (subscriber.autorisation_user_name,))[0] * ' '
                        context['spacer12'] = self.create_spacers((63,), (subscriber.autorisation_password,))[0] * ' '
                        context['spacer13'] = self.create_spacers((63,), (subscriber.display_name,))[0] * ' '
                        context['spacer14'] = self.create_spacers((63,), (subscriber.privacy,))[0] * ' '
                        i += 1
                        text += self._render('isdnport_middle', *scopes, context=dict(context, subscriber=subscriber))

                text += self._render('isdnport_bottom', *scopes, context=dict(context, port=port))
                self._write(text)
            elif self._validate((args[0],), 'pstnport') and context['path'].split('/')[-1] == 'cfgm' and \
                port.type == 'PSTN':
                context['spacer1'] = self.create_spacers((67,), (port.enable,))[0] * ' '
                context['spacer2'] = self.create_spacers((67,), (port.register_as_global,))[0] * ' '
                context['spacer3'] = self.create_spacers((67,), (port.pay_phone,))[0] * ' '
                context['spacer4'] = self.create_spacers((67,), (port.sip_profile,))[0] * ' '
                context['spacer5'] = self.create_spacers((67,), (port.proxy_registrar_profile,))[0] * ' '
                context['spacer6'] = self.create_spacers((67,), (port.codec_sdp_profile,))[0] * ' '
                context['spacer7'] = self.create_spacers((67,), (port.pstn_profile,))[0] * ' '
                context['spacer8'] = self.create_spacers((67,), (port.enterprise_profile,))[0] * ' '
                text = self._render('pstnport_top', *scopes, context=dict(context, port=port))

                i = 0
                for subscriber in self._model.subscribers:
                    if subscriber.type == 'port' and subscriber.address == self.component_name:
                        context['i'] = i
                        context['spacer10'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                        context['spacer11'] = self.create_spacers((63,), (subscriber.autorisation_user_name,))[0] * ' '
                        context['spacer12'] = self.create_spacers((63,), (subscriber.autorisation_password,))[0] * ' '
                        context['spacer13'] = self.create_spacers((63,), (subscriber.display_name,))[0] * ' '
                        context['spacer14'] = self.create_spacers((65,), (subscriber.privacy,))[0] * ' '
                        i += 1
                        text += self._render('pstnport_middle', *scopes, context=dict(context, subscriber=subscriber))

                text += self._render('pstnport_bottom', *scopes, context=dict(context, port=port))
                self._write(text)
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        pass

    def do_deleteinterface(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_createinterface(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        try:
            super().set(command, *args, context=context)
        except exceptions.CommandSyntaxError:
            if self._validate(args, *()):
                exc = exceptions.CommandSyntaxError(command=command)
                exc.template = 'syntax_error'
                exc.template_scopes = ('login', 'base', 'syntax_errors')
                raise exc
            elif self._validate(args, 'pstnport', str, str, str, str, str, str, str, str, str) and \
                    context['path'].split('/')[-1] == 'cfgm':
                enable, subident, register, phone, sip, proxy, codec, pstn, enterprise = self._dissect(args, 'pstnport',
                        str, str, str, str, str, str, str, str, str)
                try:
                    port = self.get_component()
                    enable = True if enable.lower() == 'true' else False
                    register = True if register.lower() == 'true' else False
                    phone = True if phone.lower() == 'true' else False
                    port.set_pstnport(enable, register, phone, sip, proxy, codec, pstn, enterprise)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))
            elif self._validate(args, 'pstnport', str, '{', str, str, str, str, str, '}', str, str, str, str, str, str,
                                str) and context['path'].split('/')[-1] == 'cfgm':
                enable, number, username, password, displayname, privacy, register, phone, sip, proxy, codec, pstn, enterprise = self._dissect(args, 'pstnport', str, '{', str, str, str, str, str, '}', str, str, str, str, str, str, str)
                try:
                    port = self.get_component()
                    try:
                        subscriber = self._model.get_subscriber('number', int(number))
                        subscriber.set('autorisation_user_name', username)
                        subscriber.set('autorisation_password', password)
                        subscriber.set('display_name', displayname)
                        subscriber.set('privacy', privacy)
                    except exceptions.SoftboxenError:
                        address = self.component_name
                        subscriber = self._model.add_subscriber(number=int(number), autorisation_user_name=username,
                                                                address=address, privacy=privacy, type='port',
                                                                display_name=displayname, autorisation_password=password)
                        pass
                    enable = True if enable.lower() == 'true' else False
                    register = True if register.lower() == 'true' else False
                    phone = True if phone.lower() == 'true' else False
                    port.set_pstnport(enable, register, phone, sip, proxy, codec, pstn, enterprise)
                except exceptions.SoftboxenError as exe:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))
            elif self._validate(args, 'isdnport', str, '{', str, str, str, str, str, '}', str, str, str, str, str, str,
                                str) and context['path'].split('/')[-1] == 'cfgm':
                enable, number, username, password, displayname, privacy, register, regdefault, layer1, sip, proxy, codec, isdnba = self._dissect(args, 'isdnport', str, '{', str, str, str, str, str, '}', str, str, str, str, str, str, str)
                try:
                    port = self.get_component()
                    try:
                        subscriber = self._model.get_subscriber('number', int(number))
                        assert subscriber.address == self.component_name
                        subscriber.set('autorisation_user_name', username)
                        subscriber.set('autorisation_password', password)
                        subscriber.set('display_name', displayname)
                        subscriber.set('privacy', privacy)
                    except exceptions.SoftboxenError:
                        address = self.component_name
                        subscriber = self._model.add_subscriber(number=int(number), autorisation_user_name=username,
                                                                address=address, privacy=privacy, type='port',
                                                                display_name=displayname, autorisation_password=password)
                        pass
                    except AssertionError:
                        raise exceptions.SoftboxenError()
                    enable = True if enable.lower() == 'true' else False
                    register = True if register.lower() == 'true' else False
                    regdefault = True if regdefault.lower() == 'true' else False
                    layer1 = True if layer1.lower() == 'true' else False
                    port.set_isdnport(enable, register, regdefault, layer1, sip, proxy, codec, isdnba)
                except exceptions.SoftboxenError as exe:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))
            elif self._validate(args, 'isdnport', str, str, str, str, str, str, str, str, str) and \
                    context['path'].split('/')[-1] == 'cfgm':
                enable, subident, register, regdefault, layer1, sip, proxy, codec, isdnba = self._dissect(args, 'isdnport',
                        str, str, str, str, str, str, str, str, str)
                try:
                    port = self.get_component()
                    enable = True if enable.lower() == 'true' else False
                    register = True if register.lower() == 'true' else False
                    regdefault = True if regdefault.lower() == 'true' else False
                    layer1 = True if layer1.lower() == 'true' else False
                    port.set_isdnport(enable, register, regdefault, layer1, sip, proxy, codec, isdnba)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))