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

from nesi.softbox.base_resources.cpe import CpeCollection, Cpe, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class HuaweiCpe(Cpe):
    """Represent physical cpe resource."""

    g_994_1_vendor_id = base.Field('g_994_1_vendor_id')
    g_994_1_country_code = base.Field('g_994_1_country_code')
    g_994_1_provider_code = base.Field('g_994_1_provider_code')
    g_994_1_vendor_info = base.Field('g_994_1_vendor_info')
    system_vendor_id = base.Field('system_vendor_id')
    system_country_code = base.Field('system_country_code')
    system_provider_code = base.Field('system_provider_code')
    system_vendor_info = base.Field('system_vendor_info')
    version_number = base.Field('version_number')
    version_number_oct = base.Field('version_number_oct')
    vendor_serial_number = base.Field('vendor_serial_number')
    self_test_result = base.Field('self_test_result')


class HuaweiCpeCollection(CpeCollection):
    """Represent a collection of cpes."""

    @property
    def _resource_type(self):
        return HuaweiCpe
