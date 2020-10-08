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


class PortgroupPortCommandProcessor(PortCommandProcessor):
    __name__ = 'portgroupport'
    management_functions = ('main', 'cfgm', 'status')
    access_points = ()

    from .portgroupportManagementFunctions import main
    from .portgroupportManagementFunctions import cfgm
    from .portgroupportManagementFunctions import status

    def do_get(self, command, *args, context=None):
        scopes = ('login', 'base', 'get')
        try:
            super().do_get(command, *args, context=None)
        except exceptions.CommandExecutionError:
            if self._validate((args[0],), 'SubscriberList') and context['component_path'].split('/')[-1] == 'status' and \
                    self._model.get_card('name', self._parent._parent.component_id).product == 'isdn':
                text = self._render('subscriberList_top', *scopes, context=context)
                i = 0
                for subscriber in self._model.subscribers:
                    if subscriber.type == 'port':  # TODO: show only subscriber of this port

                        context['i'] = i
                        context['spacer1'] = self.create_spacers((63,), (subscriber.number,))[0] * ' '
                        context['spacer2'] = self.create_spacers((63,), (subscriber.registration_state,))[0] * ' '
                        i += 1
                        text += self._render('subscriberList_item2', *scopes,
                                             context=dict(context, subscriber=subscriber))
                text += self._render('subscriberList_bottom', *scopes, context=context)

                self._write(text)
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))

    def _init_access_points(self, context=None):
        port = self._model.get_port('name', self._parent.component_id + '/' + self.component_id)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        scopes = ('login', 'base', 'set')
        try:
            super().set(command, *args, context=None)
        except exceptions.CommandExecutionError:
            if self._validate(args, *()):
                exc = exceptions.CommandSyntaxError(command=command)
                exc.template = 'syntax_error'
                exc.template_scopes = ('login', 'base', 'syntax_errors')
                raise exc
            elif self._validate(args, 'test', str):
                ip, = self._dissect(args, 'test', str)
                # TODO test case
                return
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))