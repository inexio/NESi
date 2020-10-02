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
