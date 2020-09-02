from nesi.softbox.api.schemas.box_schemas import *


class HuaweiBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('cpu_occupancy', 'vlan_interfaces', 'raio_anid')

    vlan_interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_vlan_interfaces', box_id='<id>')}})
