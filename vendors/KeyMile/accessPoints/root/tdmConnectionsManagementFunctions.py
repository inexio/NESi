main = {
    'General': {
        'Prop': {
            'Labels': 'rw',
            'AlarmStatus': 'r-'
        }
    }
}

cfgm = {
    'Connections': {
        'Cmd': (
            'CreateConnection',
            'CreateBulkConnection',
            'CreateAdvancedConnection',
            'DeleteConnection',
            'DeleteMultipleConnections',
            'ShowConnections',
            'SetLabel1',
            'SetLabel2'
        )
    },
    'Ctps': {
        'Cmd': (
            'ShowCtps',
        )
    },
    'Pbus': {
        'Prop': {
            'PbusUsage': 'r-'
        }
    }
}
