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

from nesi.devices.softbox.api import ma
from ..models.emu_models import Emu


class EmuSchema(ma.ModelSchema):
    class Meta:
        model = Emu
        fields = ('id', 'name', 'box', 'box_id', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_emu', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_emus', box_id='<box_id>')})


class EmusSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class EmuSchema(ma.ModelSchema):
        class Meta:
            model = Emu
            fields = ('id', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_emu', box_id='<box_id>', id='<id>')})

    members = ma.Nested(EmuSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_emus', box_id='<box_id>')})
