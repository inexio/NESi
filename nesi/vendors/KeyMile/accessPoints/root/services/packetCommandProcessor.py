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
from nesi.vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class PacketCommandProcessor(BaseCommandProcessor):
    __name__ = 'packet'
    management_functions = ('main',)
    access_points = ('1to1DoubleTag', '1to1SingleTag', 'mcast', 'nto1', 'pls', 'tls')

    from .packetManagementFunctions import main

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
            else:
                raise exceptions.CommandExecutionError(command=command, template='invalid_property',
                                                       template_scopes=('login', 'base', 'execution_errors'))
