from nesi.softbox.api.schemas.cpe_schemas import *


class HuaweiCpeSchema(CpeSchema):
    class Meta:
        model = Cpe
        fields = CpeSchema.Meta.fields + ('g_994_1_vendor_id', 'g_994_1_country_code', 'g_994_1_provider_code',
                                            'g_994_1_vendor_info', 'system_vendor_id', 'system_country_code',
                                            'system_provider_code', 'system_vendor_info', 'version_number',
                                            'version_number_oct', 'vendor_serial_number', 'self_test_result')
