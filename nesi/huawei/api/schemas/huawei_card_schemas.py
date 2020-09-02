from nesi.softbox.api.schemas.card_schemas import *


class HuaweiCardSchema(CardSchema):
    class Meta:
        model = Card
        fields = CardSchema.Meta.fields + ('board_name', 'board_status', 'sub_type_0', 'sub_type_1', 'power_status',
                                           'power_off_cause', 'power_off_time', 'temperature')
