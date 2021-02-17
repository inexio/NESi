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

from nesi.devices.softbox.api.schemas.cpe_schemas import *


class HuaweiCpeSchema(CpeSchema):
    class Meta:
        model = Cpe
        fields = CpeSchema.Meta.fields + ('g_994_1_vendor_id', 'g_994_1_country_code', 'g_994_1_provider_code',
                                            'g_994_1_vendor_info', 'system_vendor_id', 'system_country_code',
                                            'system_provider_code', 'system_vendor_info', 'version_number',
                                            'version_number_oct', 'vendor_serial_number', 'self_test_result')
