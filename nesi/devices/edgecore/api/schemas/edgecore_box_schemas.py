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

from nesi.devices.softbox.api.schemas.box_schemas import *


class EdgeCoreBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('management_start_address', 'management_end_address', 'logging_host',
                                          'loopback_detection_action', 'logging_port', 'logging_level',
                                          'sntp_server_ip', 'sntp_client', 'timezone_name', 'timezone_time',
                                          'summer_time_name', 'summer_time_region')


