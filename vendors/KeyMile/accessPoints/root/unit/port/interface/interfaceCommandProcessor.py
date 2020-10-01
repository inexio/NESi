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

    main = {}

    cfgm = {}

    pm = {}

    status = {}

    def _init_access_points(self, context=None):
        pass

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
