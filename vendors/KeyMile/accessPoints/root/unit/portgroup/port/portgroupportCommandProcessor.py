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
                    self._model.get_card('name', self._parent._parent.component_name).product in ('isdn', 'analog'):
                text = self._render('subscriberList_top', *scopes, context=context)
                i = 0
                for subscriber in self._model.get_subscribers('portgroupport_id', port.id):

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
                for subscriber in self._model.get_subscribers('portgroupport_id', port.id):
                    if subscriber.portgroupport_id == port.id:
                        context['i'] = i
                        context['spacer10'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                        context['spacer11'] = self.create_spacers((63,), (subscriber.autorisation_user_name,))[0] * ' '
                        context['spacer12'] = self.create_spacers((63,), (subscriber.autorisation_password,))[0] * ' '
                        context['spacer13'] = self.create_spacers((63,), (subscriber.display_name,))[0] * ' '
                        context['spacer14'] = self.create_spacers((65,), (subscriber.privacy,))[0] * ' '
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
                for subscriber in self._model.get_subscribers('portgroupport_id', port.id):
                    if subscriber.portgroupport_id == port.id:
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

    def _init_context(self, context=None):
        context['ls_Name'] = 'ISDN-BA'
        context['ls_MainMode'] = ''
        context['ls_EquipmentState'] = ''

    def do_deleteinterface(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def do_createinterface(self, command, *args, context=None):
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
            elif args[0] in ('pstnport', 'isdnport') and context['path'].split('/')[-1] == 'cfgm':
                enable = True if args[1].lower() == 'true' else False
                number = None
                username = ''
                password = ''
                displayname = ''
                privacy = 'None'
                index_end = 2
                if args[2] != '{}':
                    index_start = args.index('{')
                    index_end = args.index('}')
                    number = args[index_start + 1] if index_start + 1 < index_end else None
                    username = args[index_start + 2] if index_start + 2 < index_end else ''
                    password = args[index_start + 3] if index_start + 3 < index_end else ''
                    displayname = args[index_start + 4] if index_start + 4 < index_end else ''
                    privacy = args[index_start + 5] if index_start + 5 < index_end else 'None'

                register = True if args[index_end + 1].lower() == 'true' else False

                try:
                    port = self.get_component()
                    if number is not None:
                        try:
                            subscriber = self._model.get_subscriber('number', int(number))
                            if username is not None:
                                subscriber.set('autorisation_user_name', username)
                            if password is not None:
                                subscriber.set('autorisation_password', password)
                            if displayname is not None:
                                subscriber.set('display_name', displayname)
                            if privacy is not None:
                                subscriber.set('privacy', privacy)
                        except exceptions.SoftboxenError:
                            address = self.component_name
                            self._model.add_subscriber(number=int(number), autorisation_user_name=username,
                                                       address=address, privacy=privacy, display_name=displayname,
                                                       autorisation_password=password, portgroupport_id=port.id)
                        pass
                    if args[0] == 'isdnport':
                        regdefault = True if args[index_end + 2].lower().lower() == 'true' else False
                        layer1 = True if args[index_end + 3].lower() == 'true' else False
                        sip = args[index_end + 4]
                        proxy = args[index_end + 5]
                        codec = args[index_end + 6]
                        isdnba = args[index_end + 7]
                        port.set_isdnport(enable, register, regdefault, layer1, sip, proxy, codec, isdnba)
                    elif args[0] == 'pstnport':
                        phone = True if args[index_end + 2].lower() == 'true' else False
                        sip = args[index_end + 3]
                        proxy = args[index_end + 4]
                        codec = args[index_end + 5]
                        pstn = args[index_end + 6]
                        enterprise = args[index_end + 7]
                        port.set_pstnport(enable, register, phone, sip, proxy, codec, pstn, enterprise)
                except exceptions.SoftboxenError:
                    raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                           template_scopes=('login', 'base', 'execution_errors'))
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))