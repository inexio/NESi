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

from nesi.softbox.api.schemas.port_schemas import *


class KeyMilePortSchema(PortSchema):
    class Meta:
        model = Port
        fields = PortSchema.Meta.fields + ('channels', 'label1', 'label2', 'loopbacktest_state', 'melttest_state',
                                           'linetest_state', 'profile1_enable', 'profile1_name', 'profile1_elength',
                                           'profile2_enable', 'profile2_name', 'profile2_elength', 'profile3_enable',
                                           'profile3_name', 'profile3_elength', 'profile4_enable', 'profile4_name',
                                           'profile_mode', 'mode', 'flow_control')

    channels = ma.Nested(CpesSchema.CpeSchema, many=True)
