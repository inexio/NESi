from nesi.softbox.api.schemas.user_schemas import *


class EdgecoreUserSchema(UserSchema):
    class Meta:
        model = User
        fields = UserSchema.Meta.fields + ('profile',)
