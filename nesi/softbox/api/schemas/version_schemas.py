# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.softbox.api import ma
from ..models.version_models import Version


class VersionSchema(ma.ModelSchema):
    class Meta:
        model = Version
        fields = ('id', 'name', 'model_id', '_links')

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_version', id='<id>')})


class VersionsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class VersionSchema(ma.ModelSchema):
        class Meta:
            model = Version
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_version', id='<id>')})

    members = ma.Nested(VersionSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_versions')})
