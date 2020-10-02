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


class PortCommandProcessor(BaseCommandProcessor):
    __name__ = 'port'
    management_functions = ('main', 'cfgm', 'fm', 'pm', 'status')
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
        'Multicast': {
            'Prop': {
                'MaxNumberOfMulticastStreams': 'rw',
                'EnableIgmpClassifier': 'rw',
                'AllowStaticStreams': 'rw',
                'EnableFastLeave': 'rw',
                'GroupManagement': 'rw',
                'Bandwidth': 'rw'
            },
            'Cmd': (
                'GetGroupList',
            )
        },
        'Traceability': {
            'Prop': {
                'AgentRemoteId': 'rw'
            }
        },
        'Security': {
            'Prop': {
                'ServiceOptions': 'rw',
                'MaxNumberOfMac': 'rw'
            }
        },
        'AccessControl': {
            'Prop': {
                'ClassificationKey': 'rw',
                'MAT': 'rw'
            }
        },
        'RateLimiter': {
            'Prop': {
                'RateLimiting': 'rw',
                'RateLimitingCoS': 'rw'
            }
        },
        'Qos': {
            'Prop': {
                'WfqProfile': 'rw'
            }
        },
        'Wire': {
            'Prop': {
                'MeltConfiguration': 'rw'
            }
        },
        'Profiles': {
            'Prop': {
                'PortProfiles': 'rw'
            }
        },
        'Misc': {
            'Prop': {
                'SpecificDPBO': 'rw',
                'SpecificUPBO': 'rw'
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
                'Standard': 'r-',
                'PowerMgmStatus': 'r-',
                'Vdsl2Parameters': 'r-',
                'EstUPBOElectricalLength': 'r-',
                'LineRate': 'r-',
                'LineSnrMargin': 'r-',
                'AttainableNetDataRate': 'r-',
                'AttainableRate': 'r-',
                'OutputPower': 'r-',
                'BandStatus': 'r-'
            }
        },
        'statistics': {
            'Prop': {
                'counters': 'r-',
                'PolicingCounters': 'r-'
            },
            'Cmd': (
                'ResetPortCounters',
            )
        },
        'Nto1MacAccessDynamicList': {
            'Prop': {
                'UnicastList': 'r-'
            }
        },
        'HostPortStatistics': {
            'GeneralCounters': {
                'Prop': {
                    'GeneralList': 'r-'
                },
                'Cmd': (
                    'ResetGeneralCounters',
                )
            },
            'ProtocolCounters': {
                'IgmpCounters': {
                    'Prop': {
                        'IgmpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetIgmpCounters',
                        )
                    },
                'DhcpCounters': {
                    'Prop': {
                        'DhcpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetDhcpCounters',
                        )
                    },
                'ArpCounters': {
                    'Prop': {
                        'ArpProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetArpCounters',
                        )
                    },
                'PPPoECounters': {
                    'Prop': {
                        'PPPoEProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetPPPoECounters',
                        )
                    },
                'UnknownSourceMACCounters': {
                    'Prop': {
                        'UnknownSrcMACProtocolList': 'r-'
                    },
                    'Cmd': (
                        'ResetUnknownSrcMACCounters',
                    )
                },
            },
        },
        'TLSMacForwardingList': {
            'Prop': {
                'MacForwardingList': 'r-'
            },
            'Cmd': (
                'FlushMacForwardingList',
            )
        },
        '1to1MacForwardingList': {
            'Prop': {
                'One2OneMacForwardingList': 'r-'
            }
        },
        'Qos': {
            'Prop': {
                'wfqueues': 'r-'
            }
        },
        'Multicast': {
            'stream': {
                'Dynamic': {
                    'Prop': {
                        'ActiveStreams': 'r-'
                        },
                    'Cmd': (
                        'ClearActiveStreams',
                        )
                    },
                'Static': {
                    'Prop': {
                        'StaticStreams': 'r-'
                    }
                },
            },

            'Vlan': {
                'Prop': {
                    'AttachedVlans': 'r-'
                }
            },
            'Preview': {
                'Cmd': (
                    'ResetPreviewSettings',
                )
            },
            'Bandwidth': {
                'Prop': {
                    'bandwidthStatus': 'r-'
                }
            },
        },
        'LineTest': {
            'MELT': {
                'Prop': {
                    'MeltResults': 'r-'
                },
                'Cmd': (
                    'StartMeltMeasurement',
                )
            },
            'Delt': {
                'Prop': {
                    'DeltMeasurementStatus': 'r-',
                    'RecordedDeltMeasurements': 'r-'
                },
                'Cmd': (
                    'StartDeltMeasurement',
                )
            },
            'Selt': {
                'Prop': {
                    'SeltMeasurementStatus': 'r-',
                    'RecordedSeltMeasurements': 'r-',
                    'CableType': 'rw',
                    'BandplanProfile': 'rw',
                    'TargetSnrm': 'rw'
                },
                'Cmd': (
                    'StartSeltMeasurement',
                )
            },
        },
        'Defects': {
            'Prop': {
                'Defects': 'r-'
            }
        },
        'LineInventory': {
            'Prop': {
                'VendorId': 'r-'
            }
        },
        'Maintenance': {
            'Prop': {
                'DslOperationStatus': 'r-'
            }
        },
        'Subcarrier': {
            'Cmd': (
                'ShowBitAllocation',
            )
        },
        'RfiBands': {
            'Prop': {
                'NotchStatus': 'r-'
            }
        }
    }

    def _init_access_points(self, context=None):
        port = self._model.get_port('name', context['unit'] + '/' + context['port'])

        for chan in self._model.get_chans('port_id', port.id):
            identifier = 'chan-' + chan.name.split('/')[-1]
            if identifier in self.access_points:
                continue
            self.access_points += (identifier,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)