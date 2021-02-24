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

from nesi.devices.softbox.api.schemas.vlan_schemas import *


class HuaweiVlanSchema(VlanSchema):
    class Meta:
        model = Vlan
        fields = VlanSchema.Meta.fields + \
                 ('type', 'attribute', 'bind_service_profile_id', 
                  'bind_RAIO_profile_index', 'priority',
                  'native_vlan', 'tag')
