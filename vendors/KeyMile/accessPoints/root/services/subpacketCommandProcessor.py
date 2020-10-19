# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class SubpacketCommandProcessor(BaseCommandProcessor):
    __name__ = 'subpacket'
    management_functions = ('main', 'cfgm')
    access_points = ()

    from .subpacketManagementFunctions import main
    from .subpacketManagementFunctions import cfgm

    def _init_access_points(self, context=None):
        self.access_points = ()
        try:
            self.management_functions = ('main', 'cfgm')
            s_type = context['ServiceType']

            srvcs = self._model.get_srvcs('service_type', s_type)
            for srvc in srvcs:
                identifier = srvc.name
                if identifier in self.access_points:
                    continue
                self.access_points += (identifier,)
        except exceptions.InvalidInputError:
            pass

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
