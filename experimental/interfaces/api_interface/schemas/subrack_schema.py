from nesi.softbox.api import ma
from experimental.db_models.alcatel.subrack_models import AlcatelSubrack


class SubracksSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count')

    class SubrackSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelSubrack
            fields = ('id', 'name')

    members = ma.Nested(SubrackSchema, many=True)
