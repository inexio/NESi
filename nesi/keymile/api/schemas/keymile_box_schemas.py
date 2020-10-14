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

from nesi.softbox.api.schemas.box_schemas import *


class KeymileBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('channels', 'interfaces', 'currTemperature')

    interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_interfaces', box_id='<id>')}})

    channels = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_channels', box_id='<id>')}})
