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

from nesi.softbox.api.schemas.qos_interface_schemas import *


class AlcatelQosInterfaceSchema(QosInterfaceSchema):
    class Meta:
        model = QosInterface
        fields = QosInterfaceSchema.Meta.fields + \
                 ('scheduler_node', 'cac_profile', 'ds_num_rem_queue', 'us_num_queue',
                  'oper_weight', 'oper_rate', 'mc_scheduler_node', 'bc_scheduler_node',
                  'ds_schedule_tag', 'upstream_queue', 'upstream_queue_bandwidth_profile',
                  'upstream_queue_bandwidth_sharing', 'upstream_queue_priority', 'upstream_queue_weight')