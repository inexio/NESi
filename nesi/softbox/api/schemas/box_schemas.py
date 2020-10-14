# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst

from nesi.softbox.api import ma
from ..models.box_models import Box
from ..schemas.subrack_schemas import SubracksSchema
from ..schemas.credential_schemas import CredentialsSchema
from ..schemas.vlan_schemas import VlansSchema
from ..schemas.portprofile_schemas import PortProfilesSchema


class RootSchema(ma.ModelSchema):
    class Meta:
        fields = ('description', 'boxen', '_links')

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_root')})


class BoxSchema(ma.ModelSchema):
    class Meta:
        model = Box
        fields = ('id', 'vendor', 'model', 'version', 'software_version', 'network_protocol', 'network_address',
                  'network_port', 'uuid', 'description', 'interfaces', 'logports',
                  'hostname', 'mgmt_address', 'credentials', 'credential_details', 'port_profiles',
                  'port_profile_details', 'vlans', 'service_vlans', 'vlan_details', 'subscribers',
                  'subracks', 'subrack_details', 'cards', 'ports', 'channels', 'service_ports', 'emus', 'onts', 'ont_ports', 'cpes',
                  'cpe_ports', 'routes', 'login_banner', 'vlan_interfaces', 'users', 'mgmt_cards', 'mgmt_ports',
                  'welcome_banner', 'last_login', 'last_logout', 'sntp_server_ip_address', 'timezone_offset', '_links', 'currTemperature')

    credentials = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_credentials', box_id='<id>')}})

    credential_details = ma.Nested(CredentialsSchema.CredentialSchema, many=True)

    users = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_users', box_id='<id>')}})

    subracks = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_subracks', box_id='<id>')}})

    subrack_details = ma.Nested(SubracksSchema.SubrackSchema, many=True)

    cards = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_cards', box_id='<id>')}})

    mgmt_cards = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_mgmt_cards', box_id='<id>')}})

    ports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_ports', box_id='<id>')}})

    mgmt_ports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_mgmt_ports', box_id='<id>')}})

    channels = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_channels', box_id='<id>')}})

    interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_interfaces', box_id='<id>')}})

    service_ports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_service_ports', box_id='<id>')}})

    emus = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_emus', box_id='<id>')}})

    subscribers = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_subscribers', box_id='<id>')}})

    logports = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_logports', box_id='<id>')}})

    onts = ma.Hyperlinks({'_links': {
            'self': ma.URLFor('show_onts', box_id='<id>')}})

    ont_ports = ma.Hyperlinks({'_links': {
            'self': ma.URLFor('show_ont_ports', box_id='<id>')}})

    cpes = ma.Hyperlinks({'_links': {
            'self': ma.URLFor('show_cpes', box_id='<id>')}})

    cpe_ports = ma.Hyperlinks({'_links': {
            'self': ma.URLFor('show_cpe_ports', box_id='<id>')}})

    port_profiles = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_port_profiles', box_id='<id>')}})

    port_profile_details = ma.Nested(PortProfilesSchema.PortProfileSchema, many=True)

    vlans = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_vlans', box_id='<id>')}})

    service_vlans = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_service_vlans', box_id='<id>')}})

    vlan_details = ma.Nested(VlansSchema.VlanSchema, many=True)

    vlan_interfaces = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_vlan_interfaces', box_id='<id>')}})

    routes = ma.Hyperlinks(
        {'_links': {
            'self': ma.URLFor('show_routes', box_id='<id>')}})

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_box', id='<id>'),
         'collection': ma.URLFor('show_boxen')})


class BoxenSchema(ma.ModelSchema):
    class Meta:
        fields = ('members', 'count', '_links')

    class BoxSchema(ma.ModelSchema):
        class Meta:
            model = Box
            fields = (
                'id', 'vendor', 'model', 'version', 'uuid',
                '_links')

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_box', id='<id>')})

    members = ma.Nested(BoxSchema, many=True)

    _links = ma.Hyperlinks(
        {'self': ma.URLFor('show_boxen')})
