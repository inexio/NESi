from nesi.softbox.api.schemas.vlan_schemas import *


class AlcatelVlanSchema(VlanSchema):
    class Meta:
        model = Vlan
        fields = VlanSchema.Meta.fields + ('status', 'fdb_id', 'name', 'description', 'role', 'shutdown',
                                           'access_group_in', 'access_group_out', 'ip_redirect', 'ip_proxy_arp',
                                           'unicast_reverse_path_forwarding', 'load_interval', 'mpls_ip',
                                           'protocol_filter', 'pppoe_relay_tag', 'pppoe_linerate',
                                           'circuit_id_pppoe', 'remote_id_pppoe', 'access_on_port', 'trunk_on_port',
                                           'trunk_native_on_port', 'box', 'in_qos_prof_name', 'new_broadcast',
                                           'new_secure_fwd', 'dhcp_opt82_ext', 'dhcp_opt82', 'aging_time',
                                           'circuit_id_dhcp', 'remote_id_dhcp', 'mode', 'tag', 'egress_port')
