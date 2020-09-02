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

from nesi.softbox.base_resources.vlan import VlanCollection, Vlan, logging, base

LOG = logging.getLogger(__name__)


class AlcatelVlan(Vlan):
    """Represent a VLAN resource."""

    number = base.Field('number')
    status = base.Field('status')
    fdb_id = base.Field('fdb_id')
    role = base.Field('role')
    shutdown = base.Field('shutdown')
    access_group_in = base.Field('access_group_in')
    access_group_out = base.Field('access_group_out')
    ip_redirect = base.Field('ip_redirect')
    ip_proxy_arp = base.Field('ip_proxy_arp')
    unicast_reverse_path_forwarding = base.Field('unicast_reverse_path_forwarding')
    load_interval = base.Field('load_interval')
    mpls_ip = base.Field('mpls_ip')
    protocol_filter = base.Field('protocol_filter')
    pppoe_relay_tag = base.Field('pppoe_relay_tag')
    pppoe_linerate = base.Field('pppoe_linerate')
    circuit_id_pppoe = base.Field('circuit_id_pppoe')
    remote_id_pppoe = base.Field('remote_id_pppoe')
    in_qos_prof_name = base.Field('in_qos_prof_name')
    new_broadcast = base.Field('new_broadcast')
    new_secure_fwd = base.Field('new_secure_fwd')
    dhcp_opt82_ext = base.Field('dhcp_opt82_ext')
    dhcp_opt82 = base.Field('dhcp_opt82')
    aging_time = base.Field('aging_time')
    remote_id_dhcp = base.Field('remote_id_dhcp')
    circuit_id_dhcp = base.Field('circuit_id_dhcp')
    mode = base.Field('mode')
    tag = base.Field('tag')
    egress_port = base.Field('egress_port')

    def change_name(self, name):
        """Changes a vlans display name"""
        self.update(name=name)

    def set_pppoe_relay_tag(self, tag):
        """Change syslog_route value."""
        self.update(pppoe_relay_tag=tag)

    def set_protocol_filter(self, protocol_filter):
        """Change protocol filter of a vlan"""
        self.update(protocol_filter=protocol_filter)

    def set_new_broadcast(self, new_broadcast):
        """Change new_broadcast of a vlan"""
        self.update(new_broadcast=new_broadcast)

    def set_new_secure_fwd(self, new_secure_fwd):
        """Change new_secure_fwd of a vlan"""
        self.update(new_secure_fwd=new_secure_fwd)

    def set_aging_time(self, aging_time):
        """Change aging_time of a vlan"""
        self.update(aging_time=aging_time)

    def set_circuit_id_dhcp(self, circuit_id_dhcp):
        """Change circuit_id_dhcp of a vlan"""
        self.update(circuit_id_dhcp=circuit_id_dhcp)

    def set_remote_id_dhcp(self, remote_id_dhcp):
        """Change remote_id_dhcp of a vlan"""
        self.update(remote_id_dhcp=remote_id_dhcp)

    def set_dhcp_opt82_ext(self, dhcp_opt82_ext):
        """Change dhcp_opt82_ext of a vlan"""
        self.update(dhcp_opt82_ext=dhcp_opt82_ext)

    def set_dhcp_opt82(self, dhcp_opt82):
        """Change dhcp_opt82 of a vlan"""
        self.update(dhcp_opt82=dhcp_opt82)

    def set_pppoe_linerate(self, pppoe_linerate):
        """Change pppoe_linerate of a vlan"""
        self.update(pppoe_linerate=pppoe_linerate)

    def set_circuit_id_pppoe(self, circuit_id_pppoe):
        """Change circuit_id_pppoe of a vlan"""
        self.update(circuit_id_pppoe=circuit_id_pppoe)

    def set_remote_id_pppoe(self, remote_id_pppoe):
        """Change remote_id_pppoe of a vlan"""
        self.update(remote_id_pppoe=remote_id_pppoe)

    def set_mode(self, mode):
        """Change mode of a vlan"""
        self.update(mode=mode)

    def set_tag(self, tag):
        """Change tag of a vlan"""
        self.update(tag=tag)

    def set_egress_port(self, port):
        """Change egress_port of a vlan"""
        self.update(egress_port=port)

    def set_in_qos_prof_name(self, name):
        """Change in_qos_prof_name of a vlan"""
        self.update(in_qos_prof_name=name)


class AlcatelVlanCollection(VlanCollection):
    """Represent the collection of VLANs."""

    @property
    def _resource_type(self):
        return AlcatelVlan
