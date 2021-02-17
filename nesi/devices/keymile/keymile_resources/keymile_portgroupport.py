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

from nesi.devices.softbox.base_resources.service_port import logging
from nesi.devices.softbox.base_resources import base

LOG = logging.getLogger(__name__)


class KeyMilePortGroupPort(base.Resource):
    """Represent logical subscriber resource."""

    # fields
    id = base.Field('id')
    name = base.Field('name')
    operational_state = base.Field('operational_state')
    admin_state = base.Field('admin_state')
    description = base.Field('description')
    label1 = base.Field('label1')
    label2 = base.Field('label2')
    type = base.Field('type')
    enable = base.Field('enable')
    register_as_global = base.Field('register_as_global')
    register_default_number_only = base.Field('register_default_number_only')
    layer_1_permanently_activated = base.Field('layer_1_permanently_activated')
    sip_profile = base.Field('sip_profile')
    proxy_registrar_profile = base.Field('proxy_registrar_profile')
    codec_sdp_profile = base.Field('codec_sdp_profile')
    isdnba_profile = base.Field('isdnba_profile')
    pay_phone = base.Field('pay_phone')
    pstn_profile = base.Field('pstn_profile')
    enterprise_profile = base.Field('enterprise_profile')

    def set_label(self, l1, l2, desc):
        self.update(label1=l1)
        self.update(label2=l2)
        self.update(description=desc)

    def admin_up(self):
        """Set the admin port state to up"""
        self.update(admin_state='1')

    def admin_down(self):
        """Set the admin port state to down"""
        self.update(admin_state='0')

    def down(self):
        """Set the port state to down"""
        self.update(operational_state='0')

    def up(self):
        """Set the port state to down"""
        self.update(operational_state='1')

    def set_pstnport(self, enable, registerglobal, phone, sip, proxy, codec, pstn, enterprise):
        """Set the pstnport"""
        self.update(enable=enable)
        self.update(register_as_global=registerglobal)
        self.update(pay_phone=phone)
        self.update(sip_profile=sip)
        self.update(proxy_registrar_profile=proxy)
        self.update(codec_sdp_profile=codec)
        self.update(pstn_profile=pstn)
        self.update(enterprise_profile=enterprise)

    def set_isdnport(self, enable, registerglobal, regdefault, layer1, sip, proxy, codec, isdn):
        """Set the isdnport"""
        self.update(enable=enable)
        self.update(register_as_global=registerglobal)
        self.update(register_default_number_only=regdefault)
        self.update(sip_profile=sip)
        self.update(proxy_registrar_profile=proxy)
        self.update(codec_sdp_profile=codec)
        self.update(layer_1_permanently_activated=layer1)
        self.update(isdnba_profile=isdn)


class KeyMilePortGroupPortCollection(base.ResourceCollection):
    """Represent a collection of logical subscribers."""

    @property
    def _resource_type(self):
        return KeyMilePortGroupPort
