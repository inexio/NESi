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

from nesi.softbox.base_resources.ont_port import OntPort, OntPortCollection, logging, base

LOG = logging.getLogger(__name__)


class HuaweiOntPort(OntPort):
    """Represent physical ONT port resource."""

    operational_state = base.Field('operational_state')
    ont_port_index = base.Field('ont_port_index')
    ont_port_type = base.Field('ont_port_type')
    speed = base.Field('speed')
    duplex = base.Field('duplex')
    link_state = base.Field('link_state')
    ring_status = base.Field('ring_status')

    qinq_mode = base.Field('qinq_mode')
    priority_policy = base.Field('priority_policy')
    inbound = base.Field('inbound')
    outbound = base.Field('outbound')
    downstream_mode = base.Field('downstream_mode')
    mismatch_policy = base.Field('mismatch_policy')
    dscp_mapping_table_index = base.Field('dscp_mapping_table_index')
    service_type = base.Field('service_type')
    service_index = base.Field('service_index')
    s_vlan = base.Field('s_vlan')
    s_pri = base.Field('s_pri')
    c_vlan = base.Field('c_vlan')
    c_pri = base.Field('c_pri')
    encap = base.Field('encap')
    s_pri_policy = base.Field('s_pri_policy')
    igmp_mode = base.Field('igmp_mode')
    igmp_vlan = base.Field('igmp_vlan')
    igmp_pri = base.Field('igmp_pri')
    max_mac_count = base.Field('max_mac_count')
    vlan_id = base.Field('vlan_id')
    
    def down(self):
        """Change ont port admin state to down."""
        self.update(admin_state='0')
        
    def up(self):
        """Change ont port admin state to up."""
        self.update(admin_state='1')


class HuaweiOntPortCollection(OntPortCollection):
    """Represent a collection of ONT ports."""

    @property
    def _resource_type(self):
        return HuaweiOntPort
