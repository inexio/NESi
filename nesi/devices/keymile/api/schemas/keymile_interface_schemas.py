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

from nesi.devices.softbox.api.schemas.interface_schemas import *


class KeyMileInterfaceSchema(InterfaceSchema):
    class Meta:
        model = Interface
        fields = InterfaceSchema.Meta.fields + ('chan_id', 'port_id', 'logport_id', 'number_of_conn_services',
                                                'reconfiguration_allowed', 'vcc_profile', 'vlan_profile',
                                                'services_connected')
