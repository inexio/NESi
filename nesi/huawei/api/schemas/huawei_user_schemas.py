from nesi.softbox.api.schemas.user_schemas import *


class HuaweiUserSchema(UserSchema):
    class Meta:
        model = User
        fields = UserSchema.Meta.fields + ('level', 'profile', 'append_info', 'reenter_num',
                                           'reenter_num_temp')
