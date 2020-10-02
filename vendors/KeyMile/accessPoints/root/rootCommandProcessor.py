# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi import exceptions
from vendors.KeyMile.baseCommandProcessor import BaseCommandProcessor


class RootCommandProcessor(BaseCommandProcessor):
    __name__ = 'root'
    management_functions = {'main', 'cfgm', 'fm', 'status'}
    access_points = ('eoam', 'fan', 'multicast', 'services', 'tdmConnections')

    main = {
        'General': {
            'Prop': {
                'Labels': 'rw',
                'AlarmStatus': 'r-'
            }
        },
        'Inventory': {
            'Prop': {
                'EquipmentInventory': 'r-'
            }
        },
        'Logbooks': {
            'Cmd': (
                'GetAllLogbooks',
                'GetAlarmLogbook',
                'GetEventLogbook',
                'GetConfigLogbook',
                'GetEquipmentLogbook',
                'GetSessionLogbook'
            )
        },
        'NESoftwareDownload': {
            'Cmd': (
                'StartEsw',
            )
        }
    }

    cfgm = {
        'ConfigurationManagement': {
            'Prop': {
                'ConfigurationStatus': 'r-',
                'BackupDescription': 'r-'
            },
            'Cmd': (
                'Load',
                'Save',
                'Initialize',
                'ChangeDescription'
            ),
            'File': {
                'Configuration': 'rw'
            }
        },
        'ManagementInterface': {
            'Prop': {
                'IP_Address': 'rw',
                'VlanId': 'rw',
                'ManagementVlanCoS': 'rw'
            }
        },
        'Packet': {
            'Prop': {
                'Bridge': 'rw',
                'MACMovement': 'rw',
                'Traceability': 'rw',
                'PPPoA': 'rw'
            }
        },
        'SessionManagement': {
            'Prop': {
                'TelnetEnabled': 'r-',
                'SshEnabled': 'r-',
                'UsbEnabled': 'r-',
                'RetryTime': 'r-',
                'SessionmanagerTime': 'r-',
                'AuthenticationManagementInterfaces': 'r-',
                'LocalAuthenticationFallback': 'r-',
                'RadiusDefaultUserclass': 'r-'
            }
        },
        'RadiusClient': {
            'Prop': {
                'CommonRadius': 'r-',
                'PrimaryRadiusServer': 'r-',
                'AlternateRadiusServer': 'r-'
            }
        },
        'DateAndTime': {
            'SNTPClient': {
                'Prop': {
                    'OperationMode': 'rw',
                    'PrimaryServer': 'rw',
                    'SecondaryServer': 'rw',
                    'PollingInterval': 'rw',
                    'BroadcastDelay': 'rw'
                }
            },
            'TimeZone': {
                'Prop': {
                    'TimeZone': 'rw',
                    'DaylightSaving': 'r-'
                }
            },
        },
        'ProfileManagement': {
            'Prop': {
                'ProfileCpsTable': 'r-'
            },
            'Cmd': (
                'Check',
                'Delete'
            ),
            'File': {
                'Profile': 'rw',
                'Cps': 'rw'
            }
        },
        'QoS': {
            'Prop': {
                'PriorityMapping': 'rw',
                'QueueMode': 'rw'
            }
        },
        'SNMP': {
            'General': {
                'Prop': {
                    'SNMPSupport': 'rw',
                    'SNMPParameters': 'r-'
                },
                'Cmd': (
                    'SetDefaultSNMPConfigurationTables'
                )
            },
            'USM': {
                'Prop': {
                    'LocalUserTable': 'rw',
                    'RemoteUserTable': 'rw'
                }
            },
        },
        'SyslogDestinations': {
            'Destination1': {
                'Prop': {
                    'SyslogDestination1': 'rw'
                }
            },
            'Destination2': {
                'Prop': {
                    'SyslogDestination2': 'rw'
                }
            },
            'Destination3': {
                'Prop': {
                    'SyslogDestination3': 'rw'
                }
            },
            'Destination4': {
                'Prop': {
                    'SyslogDestination4': 'rw'
                }
            },
            'Destination5': {
                'Prop': {
                    'SyslogDestination5': 'rw'
                }
            },
            'Destination6': {
                'Prop': {
                    'SyslogDestination6': 'rw'
                }
            },
            'Destination7': {
                'Prop': {
                    'SyslogDestination7': 'rw'
                }
            },
            'Destination8': {
                'Prop': {
                    'SyslogDestination8': 'rw'
                }
            },
            'Destination9': {
                'Prop': {
                    'SyslogDestination9': 'rw'
                }
            },
            'Destination10': {
                'Prop': {
                    'SyslogDestination10': 'rw'
                }
            },
        },
        'SyslogSources': {
            'Prop': {
                'SyslogSourceConfiguration': 'rw'
            }
        },
        'BatteryPowerSaving': {
            'Prop': {
                'PowerSavingEnabled': 'rw',
                'PowerSavingAlarm': 'rw',
                'PowerSavingThresholds': 'rw',
                'PowerSavingUnits': 'r-'
            },
            'Cmd': (
                'PowerSavingAddUnit',
                'PowerSavingRemoveUnit'
            )
        },
        'Ipsec': {
            'Prop': {
                'Ipsec': 'rw'
            }
        },
        'TemeratureLimits': {
            'Prop': {
                'ThresholdExceed': 'rw',
                'ThresholdWarning': 'rw'
            }
        },
        'ESO': {
            'Prop': {
                'Eso1ClockSources': 'rw',
                'Eso2ClockSource': 'rw'
            }
        },
        'PETS': {
            'Prop': {
                'ClockSources': 'rw',
                'PetsClockPriority': 'rw'
            }
        }
    }

    fm = {
        'ActiveFailures': {
            'Prop': {
                'ActiveFailureTable': 'r-'
            }
        },
        'Status': {
            'Prop': {
                'AlarmStatus': 'r-'
            },
            'Cmd': (
                'Acknowledge'
            )
        },
        'Configuration': {
            'Prop': {
                'AlarmConfiguration': 'rw'
            }
        }
    }

    status = {
        'DateAndTime': {
            'Time': {
                'Prop': {
                    'Summary': 'r-'
                },
                'Cmd': (
                    'SetDateAndTime'
                )
            },
            'SNTPClient': {
                'Prop': {
                    'PrimaryServerState': 'r-',
                    'SecondaryServerState': 'r-',
                    'LastResponseTime': 'r-',
                    'LastJumpTime': 'r-',
                    'LastAdjustmentTime': 'r-'
                }
            },
        },
        'ManagementInterface': {
            'Prop': {
                'SshFingerprint': 'r-'
            },
            'Cmd': (
                'Ping'
            )
        },
        'SessionManagement': {
            'Cmd': (
                'ShowSessions'
            )
        },
        'RadiusClient': {
            'Prop': {
                'PrimaryRadiusServerStatus': 'r-',
                'AlternateRadiusServerStatus': 'r-'
            }
        },
        'Ipsec': {
            'Prop': {
                'IpsecSAStatus': 'r-'
            },
            'Cmd': (
                'GetIpsecLogbook'
            )
        },
        'Redundancy': {
            'Prop': {
                'NeConfigurationStatus': 'r-',
                'RedundancyRoles': 'r-',
                'RedundancyStatus': 'r-'
            },
            'Cmd': (
                'ManualSwitchOver',
                'ForcedSwitchOver',
                'IsolateUnits',
                'JoinUnits'
            )
        },
        'Temperature': {
            'Prop': {
                'CurrTemperature': 'r-',
                'MaxTemperature': 'r-',
                'MinTemperature': 'r-'
            },
            'Cmd': (
                'ResetMinMax'
            )
        },
        'ESO': {
            'Prop': {
                'ClockOutputEso1': 'r-',
                'ClockOutputEso2': 'r-'
            }
        },
        'PETS': {
            'Prop': {
                'PetsClockSources': 'r-',
                'PetsOperationStatus': 'r-'
            },
            'Cmd': (
                'PetsClockOperation'
            )
        }
    }

    def _init_access_points(self, context=None):
        for card in self._model.cards:
            if 'unit-' + card.name in self.access_points:
                continue
            self.access_points += ('unit-' + card.name,)

    def on_unknown_command(self, command, *args, context=None):
        raise exceptions.CommandSyntaxError(command=command)