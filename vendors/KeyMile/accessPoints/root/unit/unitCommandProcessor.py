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


class UnitCommandProcessor(BaseCommandProcessor):
    __name__ = 'unit'
    management_functions = ('main', 'cfgm', 'fm', 'status')
    access_points = () #'internalPorts', only on certain cards

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        },
        'Equipment': {
            'Prop': {
                'AssignmentStatus': 'r-',
                'CurrentStatus': 'r-'
            },
            'Cmd': (
                'Assign',
                'Unassign',
                'Restart',
                'StopInBoot'
            )
        },
        'Inventory': {
            'Prop': {
                'EquipmentInventory': 'r-'
            }
        },
        'Logbooks': {
            'Cmd': (
                'GetAlarmLogbook',
                'GetEventLogbook',
                'GetEquipmentLogbook'
            )
        },
        'Software': {
            'Prop': {
                'DiskSpace': 'r-',
                'SoftwareOnUnit': 'r-',
                'HardwareAndSoftware': 'r-',
                'Status': 'r-',
                'Configuration': 'rw'
            },
            'Cmd': (
                'DeleteSoftware',
                'StartSoftware'
            ),
            'File': {
                'Software': 'rw'
            }
        }
    }

    cfgm = {
        'Vlan': {
            'Prop': {
                'VlanCosTable': 'r-'
            }
        },
        'Security': {
            'Prop': {
                'filtering': 'rw',
                'EoamMode': 'rw'
            }
        },
        'Logon': {
            'Prop': {
                'LogonOptions': 'rw',
                'OneToOneOptions': 'rw'
            }
        },
        'Mac': {
            'Prop': {
                'MacServiceBased': 'rw'
            }
        },
        'HostPort': {
            'Prop': {
                'PolicerProfile': 'rw',
                'TrunkPolicerProfile': 'rw',
                'ProtRateLimiter': 'rw'
            }
        },
        'QoS': {
            'Prop': {
                'ColorMarking': 'rw'
            }
        },
        'Wire': {
            'General': {
                'Prop': {
                    'MeltConfiguration': 'rw'
                }
            },
            'Thresholds': {
                'Prop': {
                    'MeltAlarmThresholds': 'rw'
                }
            }
        }
    }

    fm = {
        'Status': {
            'Prop': {
                'AlarmStatus': 'r-'
            },
            'Cmd': (
                'Acknowledge'
            )
        },
        'Configuration': {
            'Prop': {
                'AlarmConfiguration': 'rw'
            }
        }
    }

    status = {
        'MacAllocationTable': {
            'Prop': {
                'MacAllocationTableEntries': 'r-'
            }
        },
        'SwitchPort': {
            'Prop': {
                'Mac': 'r-',
                'MacStatus': 'r-'
            }
        },
        'HostPortStatistics': {
            'GeneralCounters': {
                'Prop': {
                    'GeneralList': 'r-'
                },
                'Cmd': (
                    'ResetGeneralCounters'
                )
            },
            'ProtocolCounters': {
                'IgmpCounters': {
                    'Prop': {
                        'IgmpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetIgmpCounters'
                        )
                    },
                'DhcpCounters': {
                    'Prop': {
                        'DhcpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetDhcpCounters'
                        )
                    },
                'ArpCounters': {
                    'Prop': {
                        'ArpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetArpCounters'
                        )
                    },
                'PPPoECounters': {
                    'Prop': {
                        'PPPoEProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetPPPoECounters'
                        )
                    },
                'UnknownSourceMACCounters': {
                    'Prop': {
                        'UnknownSrcMACProtocolList': 'r-'
                    },
                    'Cmd': (
                        'ResetUnknownSrcMACCounters'
                    )
                },
            },
        },
        'BufferManagement': {
            'Prop': {
                'BufferMgmtStatus': 'r-'
            }
        },
        'Maintenance': {
            'Prop': {
                'MeltLineTestStatus': 'r-',
                'SearchTone': 'rw'
            },
            'Cmd': (
                'StartMeltAll',
                'StopMeltAll'
            )
        }
    }

    def _init_access_points(self, context=None):
        card = self._model.get_card('name', context['unit'])

        #if card.type == ?:
        #   self.access_points += ('internalPorts',)
        #

        for port in self._model.get_ports('card_id', card.id):
            identifier = 'port-' + port.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)