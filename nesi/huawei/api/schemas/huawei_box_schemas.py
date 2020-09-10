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

from nesi.softbox.api.schemas.box_schemas import *


class HuaweiBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('cpu_occupancy', 'vlan_interfaces', 'raio_anid', 'handshake_mode',
                                          'handshake_interval', 'interactive_mode')

    vlan_interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_vlan_interfaces', box_id='<id>')}})
