from nesi.softbox.api.schemas.ontport_schemas import *


class AlcatelOntPortSchema(OntPortSchema):
    class Meta:
        model = OntPort
        fields = OntPortSchema.Meta.fields + ('admin_state', 'operational_state', 'uni_idx', 'config_indicator',
                                              'link_status', 'speed')
