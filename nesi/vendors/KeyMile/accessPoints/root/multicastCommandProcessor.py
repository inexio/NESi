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


class MulticastCommandProcessor(BaseCommandProcessor):
    __name__ = 'multicast'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
    access_points = ()

    from .multicastManagementFunctions import main
    from .multicastManagementFunctions import cfgm
    from .multicastManagementFunctions import fm
    from .multicastManagementFunctions import pm
    from .multicastManagementFunctions import status

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        else:
            raise exceptions.CommandSyntaxError(command=command)
