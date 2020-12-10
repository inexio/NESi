from experimental.db_models.config_models import *
from experimental.db_models.base_models import BoxFunctionalities
from .credentials_models import AlcatelCredentials
from .subrack_models import AlcatelSubrack
from .card_models import AlcatelCard
from .port_models import AlcatelPort
from .cpe_models import AlcatelCpe
from .cpeport_models import AlcatelCpePort
from .ont_models import AlcatelOnt
from .ontport_models import AlcatelOntPort
from .mgmt_card_models import AlcatelMgmtCard
from .mgmt_port_models import AlcatelMgmtPort
from .user_models import AlcatelUser
from .portprofile_models import AlcatelPortProfile
from .vlan_models import AlcatelVlan
from .route_models import AlcatelRoute
from .service_port_models import AlcatelServicePort
from .service_vlan_models import AlcatelServiceVlan
import json
import uuid
from nesi import exceptions


@add_boxschema
class AlcatelBox(alcatel_base, BoxFunctionalities):
    __tablename__ = 'alcatelbox'

    id = Column(Integer(), primary_key=True)
    subracks = relationship("AlcatelSubrack", backref="AlcatelBox")
    subrack_details = relationship('AlcatelSubrack', backref='subracks')
    credentials = relationship("AlcatelCredentials", backref="AlcatelBox")
    credential_details = relationship('AlcatelCredentials', backref='credentials')
    cards = relationship('AlcatelCard', backref='AlcatelBox')
    mgmt_cards = relationship('AlcatelMgmtCard', backref='AlcatelBox')
    ports = relationship('AlcatelPort', backref='AlcatelBox')
    mgmt_ports = relationship('AlcatelMgmtPort', backref='AlcatelBox')
    cpes = relationship('AlcatelCpe', backref='AlcatelBox')
    cpe_ports = relationship('AlcatelCpePort', backref='AlcatelBox')
    onts = relationship('AlcatelOnt', backref='AlcatelBox')
    ont_ports = relationship('AlcatelOntPort', backref='AlcatelBox')
    users = relationship('AlcatelUser', backref='AlcatelBox')
    serviceports = relationship('AlcatelServicePort', backref='AlcatelBox')
    servicevlans = relationship('AlcatelServiceVlan', backref='AlcatelBox')
    port_profiles = relationship('AlcatelPortProfile', backref='AlcatelBox')
    port_profile_details = relationship('AlcatelPortProfile', backref='port_profiles')
    vlans = relationship('AlcatelVlan', backref='AlcatelBox')
    vlan_details = relationship('AlcatelVlan', backref='vlans')
    routes = relationship('AlcatelRoute', backref='AlcatelBox')

    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    version = Column(String(64), nullable=False)
    welcome_banner = Column(String)
    login_banner = Column(String)
    software_version = Column(String(64), nullable=False, default="R5.5.02")
    network_protocol = Column(Enum('telnet', 'ssh'), default='telnet')
    network_port = Column(Integer(), default=None)
    network_address = Column(String(), default=None)
    # uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid1()))
    description = Column(String())
    hostname = Column(String(64))
    mgmt_address = Column(String(32))
    default_gateway = Column(String(32), default='0.0.0.0')
    net_mask = Column(String(32), default='255.255.255.0')
    contact_person = Column(String(), default=None, nullable=True)
    isam_id = Column(String(), default=None, nullable=True)
    isam_location = Column(String(), default=None, nullable=True)
    disk_space = Column(Integer(), nullable=False, default=574423552)

    def __repr__(self):
        return "<AlcatelBox(vendor='%s', model='%s', credentials='%s' and subracks='%s')>" % \
               (self.vendor, self.model, self.credentials, self.subrack)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_fields()
        self.set_subcomponents()
        self.collect_subcomponents()

    def set_fields(self):
        self.welcome_banner = "     ___       __        ______     ___   .___________. _______  __\r\n    /   \\     |  |      /      |   /   \\  |           ||   ____||  |\r\n   /  ^  \\    |  |     |  ,----`  /  ^  \\ `---|  |----`|  |__   |  |\r\n  /  /_\\  \\   |  |     |  |      /  /_\\  \\    |  |     |   __|  |  |\r\n /  _____  \\  |  `----.|  `----./  _____  \\   |  |     |  |____ |  `----.\r\n/__/     \\__\\ |_______| \\______/__/     \\__\\  |__|     |_______||_______|"
        self.login_banner = "Welcome to Alcatel_7360"
        self.hostname = "Alcatel_7360"
        self.version = "FX-4"
        self.description = "Aclatel Switch"
        self.hostname = "Alcatel_7360"
        self.mgmt_address = "10.0.0.1"
        self.network_protocol = "telnet"
        self.network_address = "127.0.0.1"
        self.network_port = 9023
        self.software_version = "R5.5.02"

    def set_subcomponents(self):
        subracks = []
        for x in ('1/1', '1/2', '1/3'):
            subrack = AlcatelSubrack(name=x, box_id=self.id)
            subracks.append(subrack)
        self.subracks = subracks
