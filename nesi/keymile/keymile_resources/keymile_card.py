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

from nesi.softbox.base_resources.card import CardCollection, Card, logging
from nesi.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeyMileCard(Card):
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

    # Keymile ipsx2/3 card SIP specifications
    gateway_name = base.Field('gateway_name')
    home_domain = base.Field('home_domain')
    sip_port_number = base.Field('sip_port_number')
    country_code = base.Field('country_code')
    area_code = base.Field('area_code')
    retransmission_timer = base.Field('retransmission_timer')
    max_retransmission_interval = base.Field('max_retransmission_interval')
    sip_extension = base.Field('sip_extension')
    asserted_id_mode = base.Field('asserted_id_mode')
    overlap_signalling = base.Field('overlap_signalling')
    overlap_timer = base.Field('overlap_timer')
    uac_request_timer = base.Field('uac_request_timer')
    uas_request_timer = base.Field('uas_request_timer')
    session_expiration = base.Field('session_expiration')
    # Keymile ipsx2/3 card Proxy specification
    proxy_mode = base.Field('proxy_mode')
    proxy_address = base.Field('proxy_address')
    proxy_port = base.Field('proxy_port')
    proxy_address_sec = base.Field('proxy_address_sec')
    proxy_port_sec = base.Field('proxy_port_sec')
    proxy_enable = base.Field('proxy_enable')
    proxy_method = base.Field('proxy_method')
    proxy_interval = base.Field('proxy_interval')
    # Keymile ipsx2/3 card Registrar specification
    registrar_adress = base.Field('registrar_adress')
    registrar_port = base.Field('registrar_port')
    registration_mode = base.Field('registration_mode')
    registration_expiration_time = base.Field('registration_expiration_time')

    def set_sip(self, gateway_name, home_domain, sip_port_number, country_code, area_code, retransmission_timer,
                  max_retransmission_interval, sip_extension,  asserted_id_mode, overlap_signalling, overlap_timer,
                  uac_request_timer, uas_request_timer, session_expiration):
        self.update(gateway_name=gateway_name)
        self.update(home_domain=home_domain)
        self.update(sip_port_number=sip_port_number)
        self.update(country_code=country_code)
        self.update(area_code=area_code)
        self.update(retransmission_timer=retransmission_timer)
        self.update(max_retransmission_interval=max_retransmission_interval)
        self.update(sip_extension=sip_extension)
        self.update(asserted_id_mode=asserted_id_mode)
        self.update(overlap_signalling=overlap_signalling)
        self.update(overlap_timer=overlap_timer)
        self.update(uac_request_timer=uac_request_timer)
        self.update(uas_request_timer=uas_request_timer)
        self.update(session_expiration=session_expiration)


    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)

    def set_proxy(self, proxy_mode, proxy_address, proxy_port, proxy_address_sec, proxy_port_sec, proxy_enable,
                  proxy_method, proxy_interval):
        self.update(proxy_mode=proxy_mode)
        self.update(proxy_address=proxy_address)
        self.update(proxy_port=proxy_port)
        self.update(proxy_address_sec=proxy_address_sec)
        self.update(proxy_port_sec=proxy_port_sec)
        self.update(proxy_enable=proxy_enable)
        self.update(proxy_method=proxy_method)
        self.update(proxy_interval=proxy_interval)

    def set_registrar(self, registrar_adress, registrar_port, registration_mode, registration_expiration_time):
        self.update(registrar_adress=registrar_adress)
        self.update(registrar_port=registrar_port)
        self.update(registration_mode=registration_mode)
        self.update(registration_expiration_time=registration_expiration_time)


class KeyMileCardCollection(CardCollection):
    """Represent a collection of cards."""

    @property
    def _resource_type(self):
        return KeyMileCard
