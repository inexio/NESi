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

from nesi.devices.softbox.base_resources.mgmt_card import MgmtCard, MgmtCardCollection, logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeyMileMgmtCard(MgmtCard):
    """Represent physical shelf resource."""

    board_name = base.Field('board_name')
    supplier_build_state = base.Field('supplier_build_state')
    board_id = base.Field('board_id')
    hardware_key = base.Field('hardware_key')
    software = base.Field('software')
    software_name = base.Field('software_name')
    software_revision = base.Field('software_revision')
    state = base.Field('state')
    serial_number = base.Field('serial_number')
    manufacturer_name = base.Field('manufacturer_name')
    model_name = base.Field('model_name')
    short_text = base.Field('short_text')
    manufacturer_id = base.Field('manufacturer_id')
    manufacturer_part_number = base.Field('manufacturer_part_number')
    manufacturer_build_state = base.Field('manufacturer_build_state')
    customer_id = base.Field('customer_id')
    customer_product_id = base.Field('customer_product_id')
    boot_loader = base.Field('boot_loader')
    processor = base.Field('processor')
    label1 = base.Field('label1')
    label2 = base.Field('label2')
    product = base.Field('product')

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)


class KeyMileMgntCardCollection(MgmtCardCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return KeyMileMgmtCard
