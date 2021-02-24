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

from nesi.devices.softbox.api.schemas.mgmt_card_schemas import *


class KeyMileMgmtCardSchema(MgmtCardSchema):
    class Meta:
        model = MgmtCard
        fields = MgmtCardSchema.Meta.fields + ('board_name', 'supplier_build_state', 'board_id', 'hardware_key',
                                               'software','software_name', 'software_revision', 'state', 'serial_number',
                                               'manufacturer_name', 'model_name', 'short_text', 'manufacturer_id',
                                               'manufacturer_part_number', 'manufacturer_build_state', 'customer_id',
                                               'customer_product_id', 'boot_loader', 'processor', 'label1', 'label2',
                                               'product')
