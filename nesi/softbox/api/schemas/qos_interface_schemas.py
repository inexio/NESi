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
from ..models.qos_interface_models import QosInterface


class QosInterfaceSchema(ma.ModelSchema):
    class Meta:
        model = QosInterface
        fields = ('id', 'name', 'description', 'box', 'box_id',
                  '_links')

    _links = ma.Hyperlinks({
        'self': ma.URLFor(
            'show_qos_interface', box_id='<box_id>', id='<id>'),
        'collection': ma.URLFor(
            'show_qos_interfaces', box_id='<box_id>')})


class QosInterfacesSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class QosInterfaceSchema(ma.ModelSchema):
        class Meta:
            model = QosInterface
            fields = ('id', 'name', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_qos_interface', box_id='<box_id>', id='<id>')})

    members = ma.Nested(QosInterfaceSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor(
            'show_qos_interfaces', box_id='<box_id>')})
