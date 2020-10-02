main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
        }
    }
}

cfgm = {
    'Profile': {
        'Prop': {
            'ChanProfile': 'rw'
        }
    },
    'subinterface': {
        'Cmd': (
            'CreateInterface',
            'DeleteInterface'
        )
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
            'Status': 'r-'
        }
    }
}
