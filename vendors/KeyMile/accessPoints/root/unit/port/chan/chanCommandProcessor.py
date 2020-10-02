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


class ChanCommandProcessor(BaseCommandProcessor):
    __name__ = 'chan'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
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
        'Profile': {
            'Prop': {
                'ChanProfile': 'rw'
            }
        },
        'subinterface': {
            'Cmd': (
                'CreateInterface',
                'DeleteInterface'
            )
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

    pm = {
        'PerformanceMonitoring': {
            'Cmd': (
                'UserCounter',
                'GetHistory15min',
                'GetHistory24h',
                'GetAlarm15min',
                'GetAlarm24hRecursive',
                'ResetUserCounter',
                'ResetAlarm15min',
                'ResetAlarm24h'
            )
        },
        'UserCounter': {
            'Prop': {
                'UserCounterDisplayMode': 'rw',
                'UserCounterTable': 'r-'
            },
            'Cmd': (
                'UserCounterReset',
            )
        },
        'History15min': {
            'Prop': {
                'History15minDisplayMode': 'rw',
                'History15minTable': 'r-'
            }
        },
        'History24h': {
            'Prop': {
                'History24hDisplayMode': 'rw',
                'History24hTable': 'r-'
            }
        },
        'Alarm15min': {
            'Prop': {
                'Alarm15minDisplayMode': 'rw',
                'Alarm15minTable': 'r-'
            },
            'Cmd': (
                'Alarm15minReset',
            )
        },
        'Alarm24h': {
            'Prop': {
                'Alarm24hDisplayMode': 'rw',
                'Alarm24hTable': 'r-'
            },
            'Cmd': (
                'Alarm24hReset',
            )
        }
    }

    status = {
        'General': {
            'Prop': {
                'Status': 'r-'
            }
        }
    }

    def _init_access_points(self, context=None):
        chan = self._model.get_chan('name', context['unit'] + '/' + context['port'] + '/' + context['chan'])
        card = self._model.get_card('name', context['unit'])

        for interface in self._model.get_interfaces('chan_id', chan.id):
            if card.product != 'adsl':
                ap_name = 'interface-'
            else:
                ap_name = 'vcc-'
            identifier = ap_name + interface.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)