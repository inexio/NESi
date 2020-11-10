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


class KeyMileBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('channels', 'interfaces', 'currTemperature', 'logports', 'ftp_server_ip', 'ftp_login',
                                          'ftp_password')

    interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_interfaces', box_id='<id>')}})

    channels = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_channels', box_id='<id>')}})

    logports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_logports', box_id='<id>')}})
