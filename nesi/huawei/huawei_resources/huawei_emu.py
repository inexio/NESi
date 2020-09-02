from nesi.softbox.base_resources.service_port import base, logging

LOG = logging.getLogger(__name__)


class HuaweiEmu(base.Resource):
    """Represent logical emu resource."""

    #fields
    number = base.Field('number')
    name = base.Field('name')
    type = base.Field('type')
    emu_state = base.Field('emu_state')
    used = base.Field('used')
    frame_id = base.Field('frame_id')
    subnode = base.Field('subnode')
    com_port = base.Field('com_port')
    limit_state = base.Field('limit_state')
    charge_state = base.Field('charge_state')
    charge_control = base.Field('charge_control')
    module_number = base.Field('module_number')
    module_0_address = base.Field('module_0_address')
    module_0_type = base.Field('module_0_type')
    module_0_current = base.Field('module_0_current')
    module_0_voltage = base.Field('module_0_voltage')
    battery_capacity = base.Field('battery_capacity')
    battery_0_current = base.Field('battery_0_current')
    dc_voltage = base.Field('dc_voltage')



class HuaweiEmuCollection(base.ResourceCollection):
    """Represent a collection of logical emus."""

    @property
    def _resource_type(self):
        return HuaweiEmu
