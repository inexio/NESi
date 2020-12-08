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

from nesi.softbox.api.schemas.port_schemas import *


class PBNPortSchema(PortSchema):
    class Meta:
        model = Port
        fields = PortSchema.Meta.fields + ('spanning_tree_guard_root', 'switchport_trunk_vlan_allowed',
                                           'switchport_mode_trunk', 'switchport_pvid', 'no_lldp_transmit', 'pbn_speed',
                                           'switchport_block_multicast', 'switchport_rate_limit_egress',
                                           'switchport_rate_limit_ingress', 'no_pdp_enable', 'no_snmp_trap_link_status',
                                           'exclamation_mark')

    channels = ma.Nested(CpesSchema.CpeSchema, many=True)
