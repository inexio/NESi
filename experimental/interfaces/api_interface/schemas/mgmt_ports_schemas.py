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
from experimental.db_models.alcatel.mgmt_port_models import AlcatelMgmtPort


class MgmtPortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class MgmtPortSchema(ma.ModelSchema):
        class Meta:
            model = AlcatelMgmtPort
            fields = ('id', 'name', 'operational_state', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_mgmt_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(MgmtPortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_mgmt_ports', box_id='<box_id>')})
