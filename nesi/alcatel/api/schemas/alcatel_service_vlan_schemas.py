from nesi.softbox.api.schemas.service_vlan_schemas import *


class AlcatelServiceVlanSchema(ServiceVlanSchema):
    class Meta:
        model = ServiceVlan
        fields = ServiceVlanSchema.Meta.fields + ('tag', 'scope', 'l2fwder_vlan')
