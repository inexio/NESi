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
            'Acknowledge',
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
