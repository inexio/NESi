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

from nesi.devices.softbox.api.schemas.card_schemas import *


class HuaweiCardSchema(CardSchema):
    class Meta:
        model = Card
        fields = CardSchema.Meta.fields + ('board_name', 'board_status', 'sub_type_0', 'sub_type_1', 'power_status',
                                           'power_off_cause', 'power_off_time', 'temperature')
