from nesi.softbox.api import db


class ServicePort(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    admin_state = db.Column(db.Enum('0', '1', '2'), default='0')  # Alcatel: 0 => down, 1 => up, 2 => not-appl; Huawei: 0 => disable, 1 => enable
    operational_state = db.Column(db.Enum('0', '1'), default='0')  # Alcatel: 0 => down, 1 => up; Huawei: 0 => disable, 1 => enable
    connected_id = db.Column(db.Integer(), nullable=False)
    connected_type = db.Column(db.Enum('port', 'ont', 'cpe'), nullable=False)

    # Alcatel data
    pvid = db.Column(db.Integer(), default=None, nullable=True)
    max_unicast_mac = db.Column(db.Integer(), default=None, nullable=True)
    qos_profile_id = db.Column(db.Integer(), default=None, nullable=True)
    pvc = db.Column(db.Boolean(), default=False)

    # Huawei Data
    vpi = db.Column(db.String(), default='-')
    vci = db.Column(db.String(), default='-')
    flow_type = db.Column(db.Enum('vlan', 'encap', '-'), default='vlan')
    flow_para = db.Column(db.Enum('untag', 'pppoe', '-'), default='untag')
    rx = db.Column(db.Integer(), default=560)
    tx = db.Column(db.Integer(), default=520)
    rx_cttr = db.Column(db.String(), default='-')
    tx_cttr = db.Column(db.String(), default='-')
    max_mac_count = db.Column(db.Integer(), default=600)
    support_down_multicast_stream = db.Column(db.String(), default='disable')
    support_igmp_packet = db.Column(db.String(), default='disable')
    bytes_us = db.Column(db.Integer(), default=448203129)
    packets_us = db.Column(db.Integer(), default=6386689)
    bytes_ds = db.Column(db.Integer(), default=430667320)
    packets_ds = db.Column(db.Integer(), default=6493472)
    inbound_table_name = db.Column(db.String(), default='ip-traffic-table_520')
    outbound_table_name = db.Column(db.String(), default='ip-traffic-table_560')
    label = db.Column(db.String(), default='-')
    priority = db.Column(db.String(), default='-')
    pvc_bundle = db.Column(db.Enum('yes', 'no'), default='no')
    tag_transforms = db.Column(db.String(), default='default')
    description = db.Column(db.String(), nullable=True, default='')
    remote_description = db.Column(db.String(), nullable=True, default='')
    service_port_bundle = db.Column(db.String(), default='-')
    cos = db.Column(db.String(), default='-')
    static_mac = db.Column(db.String(), nullable=True, default='')
    ip_address = db.Column(db.String(), nullable=True, default='')
