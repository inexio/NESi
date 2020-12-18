main = {
        'AdminAndOperStatus': {
            'Prop': {
                'AdministrativeStatus': 'rw',
                'OperationalStatus': 'r-'
            }
        },
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
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
        'subinterface': {
            'Cmd': (
                'CreateInterface',
                'DeleteInterface'
            )
        },
        'Clock': {
            'Prop': {
                'Referenceclk': 'rw'
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
                'Dhcpv6Counters': {
                    'Prop': {
                        'Dhcpv6ProtocolList': 'r-'
                        },
                    'Cmd': (
                        'ResetDhcpv6Counters',
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
                'Ndp': {
                    'Prop': {
                        'NdpList': 'r-'
                    },
                    'Cmd': (
                        'ResetNdpCounters',
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
        'Support': {
            'Cmd': (
                'StartReport',
            ),
            'File': {
                'ReportFile': 'r-'
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
        'General': {
            'Prop': {
                'OperationalWireState': 'r-',
                'ActualStatus': 'r-',
                'DSLMode': 'r-',
                'ReferenceCLK': 'r-'
            }
        },
        'Inventory': {
            'Prop': {
                'Inventory': 'r-'
            }
        }
    }

ifMIB = {
        'Interfaces': {
            'Prop': {
                'IfTable': 'rw'
            }
        },
        'IfMIB': {
            'Objects': {
                'Prop': {
                    'XTable': 'rw',
                    'StackTable': 'rw'
                }

            }
        }
    }
