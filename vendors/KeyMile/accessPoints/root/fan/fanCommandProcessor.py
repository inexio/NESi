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


class FanCommandProcessor(BaseCommandProcessor):
    __name__ = 'fan'
    management_functions = ('main', 'cfgm', 'fm')
    access_points = ()

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        },
        'Equipment': {
            'Prop': {
                'CurrentStatus': 'r-'
            }
        },
        'Inventory': {
            'Prop': {
                'EquipmentInventory': 'r-'
            }
        }
    }

    cfgm = {
        'General': {
            'Prop': {
                'Option': 'rw'
            }
        }
    }

    fm = {
        'Status': {
            'Prop': {
                'AlarmStatus': 'r-'
            },
            'Cmd': (
                'Acknowledge',
            )
        },
        'Configuration': {
            'Prop': {
                'AlarmConfiguration': 'rw'
            }
        }
    }

    def _init_access_points(self, context=None):
        for i in range(1, 12):
            identifier = 'alarm-' + str(i)
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)
