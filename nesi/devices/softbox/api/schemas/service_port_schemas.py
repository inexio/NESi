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
from ..models.service_port_models import ServicePort


class ServicePortSchema(ma.Schema):
    class Meta:
        model = ServicePort
        fields = ('id', 'name', 'box', 'box_id', 'connected_id', 'connected_type', 'admin_state', 'operational_state',
                  '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_service_port', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_service_ports', box_id='<box_id>')})


class ServicePortsSchema(ma.Schema):
    class Meta:
        fields = ('members', 'count', '_links')

    class ServicePortSchema(ma.Schema):
        class Meta:
            model = ServicePort
            fields = ('id', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_service_port', box_id='<box_id>', id='<id>')})

    members = ma.Nested(ServicePortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_service_ports', box_id='<box_id>')})
