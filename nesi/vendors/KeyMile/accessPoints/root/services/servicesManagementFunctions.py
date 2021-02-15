main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
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
    'Prop': {
        'conflictList': 'r-'
    }
}
