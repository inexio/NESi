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


class MulticastCommandProcessor(BaseCommandProcessor):
    __name__ = 'multicast'
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
        'Multicast': {
            'General': {
                'Prop': {
                    'SnoopingMode': 'rw',
                    'LocalIPAddressForIGMPGeneration': 'rw',
                    'IPSourceAddressOfQueries': 'rw',
                    'portGroupInactivityTimeout': 'rw'
                },
                'Cmd': (
                    'CreateVlan',
                    'DeleteVlan'
                )
            },
            'PreJoin': {
                'Prop': {
                    'preJoinIntervalPeriod': 'rw'
                }
            },
            'PostLeave': {
                'Prop': {
                    'postLeaveDelayPeriod': 'rw'
                }
            },
            'Preview': {
                'Prop': {
                    'previewSettings': 'rw'
                }
            },
            'Bandwidth': {
                'Prop': {
                    'defaultBandwidthPerStream': 'rw'
                }
            },
            'Alarms': {
                'Prop': {
                    'configuredMulticastStreamsThreshold': 'rw'
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
        },
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
        }
    }

    status = {
        'multicast': {
            'activeStreams': {
                'Dynamic': {
                    'Prop': {
                        'activeMulticastStreams': 'r-',
                        'NumberOfActiveStreams': 'r-'
                        },
                    'Cmd': (
                        'clearAllStreams',
                        )
                    },
                'Static': {
                    'Prop': {
                        'StaticMulticastStreams': 'r-',
                        'NumberOfStaticStreams': 'r-'
                    }
                },
            },

            'unitConfiguration': {
                'Prop': {
                    'multicastUnitConfigurationStatus': 'r-'
                }
            },
            'portSummary': {
                'Prop': {
                    'CoreUnitFrontPorts': 'r-',
                    'CapableServiceUnits': 'r-'
                }
            },
            'Router': {
                'Prop': {
                    'learnedIpRouterSourceAddress': 'r-'
                }

            }
        }
    }

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)