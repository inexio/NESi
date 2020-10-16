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
            'Blacklist': 'rw'
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
    },
    'DuplicatedMac': {
        'Prop': {
            'DuplicatedMacAccessList': 'r-'
        },
        'Cmd': (
            'FlushMacAccessDuplicatedList',
        )
    }
}

status = {
    'DynamicList': {
        'Prop': {
            'DynamicList': 'r-'
        },
        'Cmd': (
            'FlushMacAccessDynamicList',
            'DeleteMacAccessDynamicListEntry'
        )
    },
    'UNIBlacklist': {
        'Prop': {
            'Blacklist': 'r-',
            'BNGlist': 'r-'
        },
        'Cmd': (
            'DeleteMacAccessBNGlistEntry',
        )
    }
}
