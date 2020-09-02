from nesi.softbox.api.schemas.route_schemas import *


class HuaweiRouteSchema(RouteSchema):
    class Meta:
        model = Route
        fields = RouteSchema.Meta.fields + ('sub_mask',)
