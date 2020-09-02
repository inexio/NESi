from nesi.softbox.api.schemas.subrack_schemas import *


class HuaweiSubrackSchema(SubrackSchema):
    class Meta:
        model = Subrack
        fields = SubrackSchema.Meta.fields + ('frame_status', 'temperature')
