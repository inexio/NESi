from nesi.softbox.api.schemas.box_schemas import *


class AlcatelBoxSchema(BoxSchema):
    class Meta:
        model = Box
        fields = BoxSchema.Meta.fields + ('contact_person', 'isam_id', 'isam_location',
                                          'board_missing_reporting_logging', 'download_error',
                                          'board_instl_missing_reporting_logging', 'disk_space', 'free_space',
                                          'download_progress', 'board_init_reporting_logging',
                                          'board_hw_issue_reporting_logging', 'upload_progress', 'upload_error', 'auto_activate_error',
                                          'default_route', 'logging_server_ip', 'udp_logging_server_ip',
                                          'syslog_route', 'plugin_dc_b_severity', 'public_host_address',
                                          'futurama_host_address', 'tellme_host_address', 'max_lt_link_speed',
                                          'port_num_in_proto', 'admin_slot_numbering', 'primary_file_server_id',
                                          'broadcast_frames', 'priority_policy_port_default', 'sntp_server_table',
                                          'qos_interfaces')

    qos_interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_qos_interfaces', box_id='<id>')}})
