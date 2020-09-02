from nesi.softbox.api.schemas.service_vlan_schemas import *


class HuaweiServiceVlanSchema(ServiceVlanSchema):
    class Meta:
        model = ServiceVlan
        fields = ServiceVlanSchema.Meta.fields + ('tag', 'mode')
