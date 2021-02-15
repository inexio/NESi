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
from ..models.vendor_models import Vendor
from ..schemas.model_schemas import ModelsSchema


class VendorSchema(ma.ModelSchema):
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'models', '_links')

    models = ma.Nested(ModelsSchema.ModelSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_vendor', id='<id>')})


class VendorsSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class VendorSchema(ma.ModelSchema):
        class Meta:
            model = Vendor
            fields = ('id', 'name', 'models', '_links')

        models = ma.Nested(ModelsSchema.ModelSchema, many=True)

        _links = ma.Hyperlinks(
            {'self': ma.URLFor(
                'show_vendor', id='<id>')})

    members = ma.Nested(VendorSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_vendors')})
