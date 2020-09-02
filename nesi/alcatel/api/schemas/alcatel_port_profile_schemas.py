from nesi.softbox.api.schemas.portprofile_schemas import *


class AlcatelPortProfileSchema(PortProfileSchema):
    class Meta:
        model = PortProfile
        fields = PortProfileSchema.Meta.fields + ('up_policer', 'down_policer', 'committed_info_rate',
                                                  'committed_burst_size', 'logical_flow_type')
