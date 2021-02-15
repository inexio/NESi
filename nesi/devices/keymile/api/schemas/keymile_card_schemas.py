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

from nesi.devices.softbox.api.schemas.card_schemas import *


class KeyMileCardSchema(CardSchema):
    class Meta:
        model = Card
        fields = CardSchema.Meta.fields + ('board_name', 'supplier_build_state', 'board_id', 'hardware_key', 'software',
                                           'software_name', 'software_revision', 'state', 'serial_number',
                                           'manufacturer_name', 'model_name', 'short_text', 'manufacturer_id',
                                           'manufacturer_part_number', 'manufacturer_build_state', 'customer_id',
                                           'customer_product_id', 'boot_loader', 'processor', 'label1', 'label2',
                                           'gateway_name', 'home_domain', 'sip_port_number', 'country_code', 'area_code',
                                           'retransmission_timer', 'max_retransmission_interval', 'sip_extension',
                                           'asserted_id_mode', 'overlap_signalling', 'overlap_timer',
                                           'uac_request_timer', 'uas_request_timer', 'session_expiration', 'proxy_mode',
                                           'proxy_address', 'proxy_port', 'proxy_address_sec', 'proxy_port_sec',
                                           'proxy_enable', 'proxy_method', 'proxy_interval', 'registrar_adress',
                                           'registrar_port', 'registration_mode', 'registration_expiration_time',
                                           'gateway_ipaddress', 'subnet_mask', 'default_gateway')
