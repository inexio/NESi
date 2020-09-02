from nesi.softbox.api.schemas.qos_interface_schemas import *


class AlcatelQosInterfaceSchema(QosInterfaceSchema):
    class Meta:
        model = QosInterface
        fields = QosInterfaceSchema.Meta.fields + \
                 ('scheduler_node', 'cac_profile', 'ds_num_rem_queue', 'us_num_queue',
                  'oper_weight', 'oper_rate', 'mc_scheduler_node', 'bc_scheduler_node',
                  'ds_schedule_tag', 'upstream_queue', 'upstream_queue_bandwidth_profile',
                  'upstream_queue_bandwidth_sharing', 'upstream_queue_priority', 'upstream_queue_weight')