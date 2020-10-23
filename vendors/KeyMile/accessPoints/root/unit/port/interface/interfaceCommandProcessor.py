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


class InterfaceCommandProcessor(BaseCommandProcessor):
    __name__ = 'interface'
    management_functions = ('main', 'cfgm', 'pm', 'status')
    access_points = ()

    from .interfaceManagementFunctions import main
    from .interfaceManagementFunctions import cfgm
    from .interfaceManagementFunctions import pm
    from .interfaceManagementFunctions import status

    def set(self, command, *args, context=None):
        if self._validate(args, *()):
            exc = exceptions.CommandSyntaxError(command=command)
            exc.template = 'syntax_error'
            exc.template_scopes = ('login', 'base', 'syntax_errors')
            raise exc
        elif self._validate(args, 'test', str):
            ip, = self._dissect(args, 'test', str)
            #TODO test case
            return
        else:
            raise exceptions.CommandSyntaxError(command=command)

    def get_component(self):
        return self._model.get_interface('name', self.component_name)
