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

from nesi.softbox.api.schemas.channel_schemas import *


class KeyMileChannelSchema(ChannelSchema):
    class Meta:
        model = Channel
        fields = ChannelSchema.Meta.fields + ('interfaces', 'chan_profile_name', 'curr_rate_u', 'curr_rate_d',
                                              'prev_rate_u', 'prev_rate_d', 'curr_delay_u')
