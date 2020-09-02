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

from nesi.softbox.base_resources.qos_interface import QosInterface, QosInterfaceCollection, logging, base

LOG = logging.getLogger(__name__)


class AlcatelQosInterface(QosInterface):
    """Represent a QosInterface resource."""

    scheduler_node = base.Field('scheduler_node')
    cac_profile = base.Field('cac_profile')
    ds_num_rem_queue = base.Field('ds_num_rem_queue')
    us_num_queue = base.Field('us_num_queue')
    oper_weight = base.Field('oper_weight')
    oper_rate = base.Field('oper_rate')
    mc_scheduler_node = base.Field('mc_scheduler_node')
    bc_scheduler_node = base.Field('bc_scheduler_node')
    ds_schedule_tag = base.Field('ds_schedule_tag')
    upstream_queue = base.Field('upstream_queue')
    upstream_queue_bandwidth_profile = base.Field('upstream_queue_bandwidth_profile')
    upstream_queue_bandwidth_sharing = base.Field('upstream_queue_bandwidth_sharing')
    upstream_queue_priority = base.Field('upstream_queue_priority')
    upstream_queue_weight = base.Field('upstream_queue_weight')

    def set(self, field, value):
        mapping = {field: value}
        self.update(**mapping)


class AlcatelQosInterfaceCollection(QosInterfaceCollection):
    """Represent the collection of QosInterfaces."""

    @property
    def _resource_type(self):
        return AlcatelQosInterface
