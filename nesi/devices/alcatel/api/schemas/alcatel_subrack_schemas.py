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

from nesi.devices.softbox.api.schemas.subrack_schemas import *


class AlcatelSubrackSchema(SubrackSchema):
    class Meta:
        model = Subrack
        fields = SubrackSchema.Meta.fields + ('planned_type', 'actual_type', 'admin_state', 'operational_state',
                                              'err_state', 'availability', 'mode', 'subrack_class', 'serial_no',
                                              'variant', 'ics', 'enabled')
