from nesi.softbox.api.schemas.service_port_schemas import *


class AlcatelServicePortSchema(ServicePortSchema):
    class Meta:
        model = ServicePort
        fields = ServicePortSchema.Meta.fields + ('max_unicast_mac', 'qos_profile_id', 'pvid', 'pvc')
