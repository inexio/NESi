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
    'DefaultMdLevel': {
        'Prop': {
            'DefaultMdSettings': 'rw'
        }
    },
    'ContextMap': {
        'Prop': {
            'Mapping': 'rw'
        }
    },
    'Aggregation': {
        'Prop': {
            'Role': 'rw',
            'Address': 'rw'
        }
    },
    'Md': {
        'Cmd': (
            'CreateMd',
            'DeleteMd'
        )
    }
}

status = {
    'DefaultMdMips': {
        'Prop': {
            'Mips': 'r-'
        }
    },
    'ConfigurationErrors': {
        'Prop': {
            'InterfacesInError': 'r-'
        }
    }
}
