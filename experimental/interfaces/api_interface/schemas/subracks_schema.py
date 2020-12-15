from nesi.softbox.api import ma
from experimental.db_models.alcatel.subrack_models import AlcatelSubrack


class SubracksSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class SubrackSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelSubrack
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_subrack', box_id='<box_id>', id='<id>')})

    members = ma.Nested(SubrackSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_subracks', box_id='<box_id>')})
