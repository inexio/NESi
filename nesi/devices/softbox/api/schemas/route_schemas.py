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
from ..models.route_models import Route


class RouteSchema(ma.ModelSchema):
    class Meta:
        model = Route
        fields = ('id', 'dst', 'gw', 'metric', 'box', 'box_id', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_route', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_routes', box_id='<box_id>')})


class RoutesSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class RouteSchema(ma.ModelSchema):
        class Meta:
            model = Route
            fields = ('id', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_route', box_id='<box_id>', id='<id>')})

    members = ma.Nested(RouteSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_routes', box_id='<box_id>')})
