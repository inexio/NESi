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
from ..models.srvc_models import Srvc


class SrvcSchema(ma.ModelSchema):
    class Meta:
        model = Srvc
        fields = ('id', 'box', 'box_id', 'name', 'service_type', 'address', 'svid', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_srvc', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_srvcs', box_id='<box_id>')})


class SrvcsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class SrvcSchema(ma.ModelSchema):
        class Meta:
            model = Srvc
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_srvc', box_id='<box_id>', id='<id>')})

    members = ma.Nested(SrvcSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_srvcs', box_id='<box_id>')})
