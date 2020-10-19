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
                                           'linetest_state')

    channels = ma.Nested(CpesSchema.CpeSchema, many=True)
