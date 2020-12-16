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
from experimental.db_models.alcatel.portprofile_models import AlcatelPortProfile


class PortProfilesSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class PortProfileSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelPortProfile
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_port_profile', box_id='<box_id>', id='<id>')})

    members = ma.Nested(PortProfileSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor(
            'show_port_profiles', box_id='<box_id>')})
