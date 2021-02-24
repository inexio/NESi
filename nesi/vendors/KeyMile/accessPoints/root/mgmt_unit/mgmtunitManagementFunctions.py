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
        'Filter': {
            'Prop': {
                'BroadcastFilter': 'rw'
            }
        },
        'PriorityMapping': {
            'Prop': {
                'DSCPTo802Dot1qPriorityMapping': 'rw'
            }
        },
        'PacketBuffer': {
            'Prop': {
                'PacketBufferProfileName': 'rw'
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
        }
    }

status = {
        'QoS': {
            'Prop': {
                'QosPriorityMappingStatus': 'r-'
            }
        },
        'PacketBuffer': {
            'Prop': {
                'PacketBufferStatus': 'r-'
            }
        },
        'Redundancy': {
            'Prop': {
                'Status': 'r-'
            }
        }
    }
