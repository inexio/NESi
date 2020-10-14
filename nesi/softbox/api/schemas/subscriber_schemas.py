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
from ..models.subscriber_models import Subscriber


class SubscriberSchema(ma.ModelSchema):
    class Meta:
        model = Subscriber
        fields = ('id', 'name', 'box', 'box_id', 'number', 'type', 'address', 'registration_state', 'display_name',
                  'autorisation_user_name', 'autorisation_password', 'privacy',
                  '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_subscriber', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_subscribers', box_id='<box_id>')})


class SubscribersSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class SubscriberSchema(ma.ModelSchema):
        class Meta:
            model = Subscriber
            fields = ('id', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_subscriber', box_id='<box_id>', id='<id>')})

    members = ma.Nested(SubscriberSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_subscribers', box_id='<box_id>')})
