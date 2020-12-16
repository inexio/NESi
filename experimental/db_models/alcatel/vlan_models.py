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
import uuid


from experimental.db_models.config_models import *


@add_vlanschema
class AlcatelVlan(alcatel_base):
    __tablename__ = 'alcatelvlan'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64), nullable=False)
    number = Column(Integer(), nullable=False)
    description = Column(String())
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))

    # data
    # pending is just a placeholder for status value
    role = Column(Enum('access', 'trunk', 'native'), nullable=False, default='access')
    status = Column(Enum('learned', 'pending'), default='learned')
    tag = Column(Enum('tagged', 'untagged', 'single-tagged'), default='untagged')
    egress_port = Column(String(), default='')
    fdb_id = Column(Integer, default=2620)
    shutdown = Column(Boolean(), default=False)
    mtu = Column(Integer(), default=1500)
    access_group_in = Column(String(64), default='')
    access_group_out = Column(String(64), default='')
    ip_redirect = Column(Boolean(), default=False)
    ip_proxy_arp = Column(Boolean(), default=False)
    unicast_reverse_path_forwarding = Column(Boolean(), default=False)
    load_interval = Column(Integer(), default=100)
    mpls_ip = Column(String(32), default='10.1.1.12')
    protocol_filter = Column(String(32), default=None)
    pppoe_relay_tag = Column(String(32), default=None)
    pppoe_linerate = Column(String(32), default=None)
    circuit_id_pppoe = Column(String(32), default=None)
    remote_id_pppoe = Column(String(32), default=None)

    in_qos_prof_name = Column(String(), default=None)
    new_broadcast = Column(Enum('enable', 'disable'), default='disable')
    new_secure_fwd = Column(Enum('enable', 'disable'), default='disable')
    dhcp_opt82 = Column(Enum('enable', 'disable'), default='disable')
    dhcp_opt82_ext = Column(Enum('enable', 'disable'), default='disable')
    aging_time = Column(Integer(), nullable=True)
    circuit_id_dhcp = Column(String(32), default=None)
    remote_id_dhcp = Column(String(32), default=None)
    mode = Column(Enum('residential-bridge', 'reserved'), default='residential-bridge')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return "<AlcatelVlan(id='%s', name='%s', box_id='%s')>" %\
               (self.id, self.name, self.box_id)
