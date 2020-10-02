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


class ServicesMacAccessCtrlCommandProcessor(BaseCommandProcessor):
    __name__ = 'servicesMacAccessCtrl'
    management_functions = ('main', 'cfgm', 'fm', 'status')
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
        'General': {
            'Prop': {
                'Blacklist': 'rw'
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
        },
        'DuplicatedMac': {
            'Prop': {
                'DuplicatedMacAccessList': 'r-'
            },
            'Cmd': (
                'FlushMacAccessDuplicatedList',
            )
        }
    }

    status = {
        'DynamicList': {
            'Prop': {
                'DynamicList': 'r-'
            },
            'Cmd': (
                'FlushMacAccessDynamicList',
                'DeleteMacAccessDynamicListEntry'
            )
        },
        'UNIBlacklist': {
            'Prop': {
                'Blacklist': 'r-',
                'BNGlist': 'r-'
            },
            'Cmd': (
                'DeleteMacAccessBNGlistEntry',
            )
        }
    }

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)