# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.softbox.api import ma
from experimental.db_models.alcatel.alcatel_models import AlcatelBox


class BoxenSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelBox
            fields = (
                'id', 'vendor', 'model', 'version', 'uuid',
                '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>')})

    members = ma.Nested(BoxSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_boxen')})
