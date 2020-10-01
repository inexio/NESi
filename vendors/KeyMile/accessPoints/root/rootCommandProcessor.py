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


class RootCommandProcessor(BaseCommandProcessor):
    __name__ = 'root'
    management_functions = {'main', 'cfgm', 'fm', 'status'}
    access_points = ('eoam', 'fan', 'multicast', 'services', 'tdmConnections')

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        },
        'Inventory': {
            'Prop': {
                'EquipmentInventory': 'r-'
            }
        },
        'Logbooks': {
            'Cmd': (
                'GetAllLogbooks',
                'GetAlarmLogbook',
                'GetEventLogbook',
                'GetConfigLogbook',
                'GetEquipmentLogbook',
                'GetSessionLogbook'
            )
        },
        'NESoftwareDownload': {
            'Cmd': (
                'StartEsw',
            )
        }
    }

    cfgm = {}

    fm = {}

    status = {
        'DateAndTime': {
            'Time': {
                'Cmd': (
                    'SetDateAndTime',
                ),
                'Prop': {
                    'Summary': 'r-'
                }
            },
            'SNTPClient': {
                'Prop': {
                    'PrimaryServerState': 'r-'
                }
            }
        }
    }

    def _init_access_points(self, context=None):
        for card in self._model.cards:
            if 'unit-' + card.name in self.access_points:
                continue
            self.access_points += ('unit-' + card.name,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)