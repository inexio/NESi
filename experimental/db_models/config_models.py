from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Boolean, FLOAT, Float
from sqlalchemy.ext.declarative import declarative_base as db
from sqlalchemy.orm import sessionmaker, relationship
from nesi.softbox.api import ma


alcatel_base = db()
huawei_base = db()
alcatel_engine = create_engine('sqlite:///experimental/db_models/alcatel.db')
huawei_engine = create_engine('sqlite:///experimental/db_models/huawei.db')
Session = sessionmaker()


def add_boxschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls

        subracks = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_subracks', box_id='<id>')}})

        cards = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_cards', box_id='<id>')}})

        from experimental.interfaces.api_interface.schemas.subracks_schema import SubracksSchema

        subrack_details = ma.Nested(SubracksSchema.SubrackSchema, many=True)

    cls.Schema = Schema
    return cls


def add_subrackschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_subrack', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_subracks', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.cards_schemas import CardsSchema
        from experimental.interfaces.api_interface.schemas.mgmt_cards_schemas import MgmtCardsSchema
        cards = ma.Nested(CardsSchema.CardSchema, many=True)
        mgmt_cards = ma.Nested(MgmtCardsSchema.MgmtCardSchema, many=True)

    cls.Schema = Schema
    return cls


def add_cardschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

    cls.Schema = Schema
    return cls


def add_portschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_ports', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.cpes_schemas import CpesSchema
        from experimental.interfaces.api_interface.schemas.onts_schemas import OntsSchema
        #from experimental.interfaces.api_interface.schemas.mgmt_card_schemas import MgmtCardsSchema
        #from experimental.interfaces.api_interface.schemas.mgmt_card_schemas import MgmtCardsSchema
        cpes = ma.Nested(CpesSchema.CpeSchema, many=True)
        onts = ma.Nested(OntsSchema.OntSchema, many=True)
        #channels = ma.Nested(ChannelsSchema.ChannelSchema, many=True)
        #interfaces = ma.Nested(InterfacesSchema.InterfaceSchema, many=True)

    cls.Schema = Schema
    return cls


def add_cpeschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_cpe', box_id='<box_id>', id='<id>')})

        from experimental.interfaces.api_interface.schemas.cpeports_schemas import CpePortsSchema
        cpe_ports = ma.Nested(CpePortsSchema.CpePortSchema, many=True)

    cls.Schema = Schema
    return cls


def add_cpeportschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_cpe_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_cpe_ports', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_credentialschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_credential', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_credentials', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.users_schemas import UsersSchema
        user = ma.Nested(UsersSchema.UserSchema, many=True)

    cls.Schema = Schema
    return cls


def add_mgmtcardschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_mgmt_card', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_mgmt_cards', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.mgmt_ports_schemas import MgmtPortsSchema
        mgmt_ports = ma.Nested(MgmtPortsSchema.MgmtPortSchema, many=True)

    cls.Schema = Schema
    return cls


def add_mgmtportschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_mgmt_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_mgmt_ports', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_ontschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_ont', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_onts', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.ontports_schemas import OntPortsSchema
        ont_ports = ma.Nested(OntPortsSchema.OntPortSchema, many=True)

    cls.Schema = Schema
    return cls


def add_ontportschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_ont_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_ont_ports', box_id='<box_id>')})

        from experimental.interfaces.api_interface.schemas.cpes_schemas import CpesSchema
        cpes = ma.Nested(CpesSchema.CpeSchema, many=True)

    cls.Schema = Schema
    return cls


def add_vlanschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks({
            'self': ma.URLFor(
                'show_vlan', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor(
                'show_vlans', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_portprofileschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        _links = ma.Hyperlinks({
            'self': ma.URLFor(
                'show_port_profile', box_id='<box_id>', id='<id>'),
            'collection': ma.URLFor(
                'show_port_profiles', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_routeschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_route', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_routes', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_serviceportschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_service_port', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_service_ports', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_servicevlanschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_service_vlan', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_service_vlans', box_id='<box_id>')})

    cls.Schema = Schema
    return cls


def add_userschema(cls):
    class Schema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            include_fk = True

        box = ma.Hyperlinks(
            {'_links': {
                'self': ma.URLFor('show_box', id='<box_id>')}})

        _links = ma.Hyperlinks(
            {'self': ma.URLFor('show_user', box_id='<box_id>', id='<id>'),
             'collection': ma.URLFor('show_users', box_id='<box_id>')})

    cls.Schema = Schema
    return cls
