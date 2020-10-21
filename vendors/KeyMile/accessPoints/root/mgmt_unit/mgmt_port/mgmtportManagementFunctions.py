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
        },
        'SFP': {
            'Prop': {
                'EquipmentInventory': 'r-'
            }
        }
    }

cfgm = {
        'PortMode': {
            'Prop': {
                'PortMode': 'rw',
                'Redundancy': 'rw',
                'PortVlan': 'rw',
                'MTUSize': 'rw'
            }
        },
        'Rstp': {
            'Prop': {
                'Rstp': 'rw',
                'RstpParams': 'rw'
            }
        },
        'VlanList': {
            'Prop': {
                'ManagementVlan': 'r-',
                'ListType': 'rw',
                'VlanList': 'rw'
            },
            'Cmd': (
                'FlushVlanList',
            )
        },
        'QoS': {
            'Prop': {
                'SchedulingProfileName': 'rw'
            }
        },
        'Multicast': {
            'Prop': {
                'EnableIgmpClassifier': 'rw',
                'AllowStaticStreams': 'rw',
                'MulticastPortMode': 'rw'
            }
        },
        'LinkAggregation': {
            'Prop': {
                'LinkAggregation': 'rw'
            }
        },
        'PHY': {
            'Prop': {
                'PhyMode': 'rw',
                'PhyFlowControl': 'rw'
            }
        },
        'Eoam': {
            'Prop': {
                'NetworkNetworkInterface': 'rw'
            }
        },
        'PriorityMapping': {
            'Prop': {
                'DSCPTo802Dot1qTxPriorityMapping': 'rw'
            }
        },
        'Mirroring': {
            'Prop': {
                'MirrorPortList': 'rw'
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
        'PortMode': {
            'Prop': {
                'DefaultConfigEnabled': 'r-'
            }
        },
        'MAC': {
            'Prop': {
                'PortMacStatus': 'r-'
            }
        },
        'Phy': {
            'Prop': {
                'PortLinkStatus': 'r-'
            }
        },
        'Rstp': {
            'Prop': {
                'PortRstpStatus': 'r-'
            }
        },
        'LinkAggregation': {
            'Prop': {
                'Status': 'r-'
            }
        },
        'Ddm': {
            'Prop': {
                'DdmStatus': 'r-'
            }
        },
        'QoS': {
            'Prop': {
                'QosStatus': 'r-'
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

            }
        }
    }
