from nesi.softbox.api.schemas.subrack_schemas import *


class AlcatelSubrackSchema(SubrackSchema):
    class Meta:
        model = Subrack
        fields = SubrackSchema.Meta.fields + ('planned_type', 'actual_type', 'admin_state', 'operational_state',
                                              'err_state', 'availability', 'mode', 'subrack_class', 'serial_no',
                                              'variant', 'ics', 'enabled')
