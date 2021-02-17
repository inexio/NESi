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
