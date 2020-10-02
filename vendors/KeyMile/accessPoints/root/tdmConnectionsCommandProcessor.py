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


class TdmConnectionsCommandProcessor(BaseCommandProcessor):
    __name__ = 'tdmConnections'
    management_functions = ('main', 'cfgm')
    access_points = ()

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        }
    }

    cfgm = {
        'Connections': {
            'Cmd': (
                'CreateConnection',
                'CreateBulkConnection',
                'CreateAdvancedConnection',
                'DeleteConnection',
                'DeleteMultipleConnections',
                'ShowConnections',
                'SetLabel1',
                'SetLabel2'
            )
        },
        'Ctps': {
            'Cmd': (
                'ShowCtps',
            )
        },
        'Pbus': {
            'Prop': {
                'PbusUsage': 'r-'
            }
        }
    }

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)