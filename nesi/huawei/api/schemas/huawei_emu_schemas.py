from nesi.softbox.api.schemas.emu_schemas import *


class HuaweiEmuSchema(EmuSchema):
    class Meta:
        model = Emu
        fields = EmuSchema.Meta.fields + ('number', 'name', 'type', 'emu_state', 'used', 'frame_id', 'subnode',
                                          'com_port', 'limit_state', 'charge_state', 'charge_control', 'module_number',
                                          'module_0_address', 'module_0_type', 'module_0_current', 'module_0_voltage',
                                          'battery_capacity', 'battery_0_current', 'dc_voltage')
