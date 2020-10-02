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


class EoamCommandProcessor(BaseCommandProcessor):
    __name__ = 'eoam'
    management_functions = ('main', 'cfgm', 'status')
    access_points = ()

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        },
        'AdminAndOperStatus': {
            'Prop': {
                'AdministrativeStatus': 'rw',
                'OperationalStatus': 'r-'
            }
        }
    }

    cfgm = {
        'DefaultMdLevel': {
            'Prop': {
                'DefaultMdSettings': 'rw'
            }
        },
        'ContextMap': {
            'Prop': {
                'Mapping': 'rw'
            }
        },
        'Aggregation': {
            'Prop': {
                'Role': 'rw',
                'Address': 'rw'
            }
        },
        'Md': {
            'Cmd': (
                'CreateMd',
                'DeleteMd'
            )
        }
    }

    status = {
        'DefaultMdMips': {
            'Prop': {
                'Mips': 'r-'
            }
        },
        'ConfigurationErrors': {
            'Prop': {
                'InterfacesInError': 'r-'
            }
        }
    }

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)