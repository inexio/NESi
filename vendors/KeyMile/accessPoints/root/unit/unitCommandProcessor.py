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


class UnitCommandProcessor(BaseCommandProcessor):
    __name__ = 'unit'
    management_functions = ('main', 'cfgm', 'fm', 'status')
    access_points = () #'internalPorts', only on certain cards

    from .unitManagementFunctions import main
    from .unitManagementFunctions import cfgm
    from .unitManagementFunctions import fm
    from .unitManagementFunctions import status

    def _init_access_points(self, context=None):
        card = self._model.get_card('name', context['unit'])

        #if card.type == ?:
        #   self.access_points += ('internalPorts',)
        #

        for port in self._model.get_ports('card_id', card.id):
            identifier = 'port-' + port.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

        # todo: add portgroup to access_points

    def do_get(self, command, *args, context=None):
        scopes = ('login', 'base', 'get')
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate((args[0],), 'SubscriberList') and context['path'].split('/')[-1] == 'status' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name', context['unit']).product == 'analog'):
            text = self._render('subscriberList_top', *scopes, context=context)
            i = 0
            for subscriber in self._model.subscribers:
                if subscriber.type == 'unit':
                    context['i'] = i
                    context['spacer1'] = self.create_spacers((63,), (subscriber.number, ))[0] * ' '
                    context['spacer2'] = self.create_spacers((63,), (subscriber.registration_state, ))[0] * ' '
                    context['spacer3'] = self.create_spacers((63,), (subscriber.address, ))[0] * ' '

                    i += 1
                    text += self._render('subscriberList_item', *scopes, context=dict(context, subscriber=subscriber))
            text += self._render('subscriberList_bottom', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'SIP') and context['path'].split('/')[-1] == 'cfgm' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name', context['unit']).product == 'analog'):
            # TODO: dynamic fields
            text = self._render('sip', *scopes, context=context)
            self._write(text)
        elif self._validate((args[0],), 'IP') and context['path'].split('/')[-1] == 'cfgm' and \
                (self._model.get_card('name', context['unit']).product == 'isdn' or self._model.get_card('name', context['unit']).product == 'analog'):
            # TODO: dynamic fields
            text = self._render('ip', *scopes, context=context)
            self._write(text)
        else:
            raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                   template_scopes=('login', 'base', 'execution_errors'))

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
