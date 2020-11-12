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


class LogportsCommandProcessor(BaseCommandProcessor):
    __name__ = 'logports'
    management_functions = ('main', 'cfgm')
    access_points = ()

    from .logportsManagementFunctions import main
    from .logportsManagementFunctions import cfgm

    def _init_access_points(self, context=None):    # work in progress
        self.access_points = ()
        card = self._model.get_card('name', self.component_name.split('/')[0])

        for logport in self._model.get_logports('card_id', card.id):
            if logport.name.count('/') == 2:
                identifier = 'logport-' + logport.name.split('/')[-1]
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)
        accpoint = list(self.access_points)
        accpoint.sort(key=lambda x: int(x.split('-')[1]))
        self.access_points = tuple(accpoint)

    def do_delete(self, command, *args, context=None):
        if self._validate(args, str) and context['path'].split('/')[-1] == 'cfgm':
            name, = self._dissect(args, str)
            if name.startswith('logport-'):
                id = name.split('-')[1]
                try:
                    port = self._model.get_logport('name', self._parent.component_name + '/L/' + id)
                    port.delete()
                except exceptions.SoftboxenError:
                    raise exceptions.CommandSyntaxError(command=command)
            else:
                raise exceptions.CommandSyntaxError(command=command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def do_create(self, command, *args, context=None):
        if self._validate(args, str, str, str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            p1, p2, p3, p4, profile = self._dissect(args, str, str, str, str, str)
            self.create(p1, p2, p3, p4, profile, command)
        elif self._validate(args, str, str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            p1, p2, p3, profile = self._dissect(args, str, str, str, str)
            self.create(p1, p2, p3, '', profile, command)
        elif self._validate(args, str, str, str) and context['path'].split('/')[-1] == 'cfgm':
            p1, p2, profile = self._dissect(args, str, str, str)
            self.create(p1, p2, '', '', profile, command)
        elif self._validate(args, str, str) and context['path'].split('/')[-1] == 'cfgm':
            p1, profile = self._dissect(args, str, str)
            self.create(p1, '', '', '', profile, command)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def create(self, p1, p2, p3, p4, profile, command):
        ids = []
        ids.append(int(p1.split('-')[1])) if p1.startswith('port-') else ids
        ids.append(int(p2.split('-')[1])) if p2.startswith('port-') else ids
        ids.append(int(p3.split('-')[1])) if p3.startswith('port-') else ids
        ids.append(int(p4.split('-')[1])) if p4.startswith('port-') else ids
        if len(ids) > 0:
            ids.sort()
            try:
                for x in ids:
                    self._model.get_logport('name', self._parent.component_name + '/L/' + str(x))
                    break
            except exceptions.SoftboxenError:
                name = self._parent.component_name + '/L/' + str(ids[0])
                ports = 'ports: '
                for x in ids:
                    ports += str(x) + ', '
                card = self._model.get_card('name', self._parent.component_name)
                logport = self._model.add_logport(card_id=card.id, name=name, ports=ports[:-2])
                logport = self._model.get_logport('name', name)
                logport.set_profile(profile)
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        else:
            raise exceptions.CommandSyntaxError(command=command)
