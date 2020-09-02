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
from ..models.credential_models import Credential


class CredentialSchema(ma.ModelSchema):
    class Meta:
        model = Credential
        fields = ('id', 'protocol', 'credential', 'username', 'password',
                  'box', '_links')

    box = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_box', id='<box_id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_credential', box_id='<box_id>', id='<id>'),
         'collection': ma.URLFor('show_credentials', box_id='<box_id>')})


class CredentialsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class CredentialSchema(ma.ModelSchema):
        class Meta:
            model = Credential
            fields = ('id', 'username', 'password', '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_credential', box_id='<box_id>', id='<id>')})

    members = ma.Nested(CredentialSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_credentials', box_id='<box_id>')})
