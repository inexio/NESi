main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
        }
    }
}

cfgm = {
    'Traceability': {
        'Prop': {
            'AutomaticAgentCircuitId': 'rw',
            'AgentCircuitId': 'rw'
        }
    },
    'Filter': {
        'Prop': {
            'MACSourceFilteringMode': 'rw',
            'MacAccessWhitelist': 'rw',
            'NumberOfMacForFloodingPrev': 'rw',
            'L2CPFilter': 'rw',
            'DestMacBlacklistProfile': 'rw',
            'SrcMacBlacklist': 'rw'
        }
    },
    'IfRateLimiter': {
        'Prop': {
            'IfRateLimiting': 'rw'
        }
    },
    'Profiles': {
        'Prop': {
            'configuredProfiles': 'rw'
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
    'ServiceInfo': {
        'Prop': {
            'ServiceStatus': 'r-'
        }
    },
    'UserConnection': {
        'Prop': {
            'CurrentPppConnectionState': 'r-'
        }
    }
}
