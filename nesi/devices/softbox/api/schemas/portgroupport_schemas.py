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
from ..models.portgroupport_models import PortGroupPort
from .subscriber_schemas import SubscribersSchema


class PortGroupPortSchema(ma.ModelSchema):
    class Meta:
        model = PortGroupPort
        fields = ('id', 'name', 'box_id', 'card_id', 'operational_state', 'admin_state', 'description', 'label1',
                  'label2', 'type', 'enable', 'register_as_global', 'subscribers',
                  'register_default_number_only', 'layer_1_permanently_activated', 'sip_profile', 'isdnba_profile',
                  'proxy_registrar_profile', 'codec_sdp_profile', 'pay_phone', 'pstn_profile', 'enterprise_profile',
                  '_links')

    subscribers = ma.Nested(SubscribersSchema.SubscriberSchema, many=True)

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_portgroupport', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_portgroupports', box_id='<box_id>')})


class PortGroupPortsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class PortGroupPortSchema(ma.ModelSchema):
        class Meta:
            model = PortGroupPort
            fields = ('id', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_portgroupport', box_id='<box_id>', id='<id>')})

    members = ma.Nested(PortGroupPortSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_portgroupports', box_id='<box_id>')})
