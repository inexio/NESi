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

from nesi.softbox.api.schemas.portprofile_schemas import *


class AlcatelPortProfileSchema(PortProfileSchema):
    class Meta:
        model = PortProfile
        fields = PortProfileSchema.Meta.fields + ('up_policer', 'down_policer', 'committed_info_rate',
                                                  'committed_burst_size', 'logical_flow_type')
