main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
        }
    },
    'Equipment': {
        'Prop': {
            'CurrentStatus': 'r-'
        }
    },
    'Inventory': {
        'Prop': {
            'EquipmentInventory': 'r-'
        }
    }
}

cfgm = {
    'General': {
        'Prop': {
            'Option': 'rw'
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
