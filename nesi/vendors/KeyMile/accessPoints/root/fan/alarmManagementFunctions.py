main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
        }
    }
}

cfgm = {
    'General': {
        'Prop': {
            'Polarity': 'rw'
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
