from experimental.db_models.base_models import *
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
import json
import uuid


class AlcatelBox(alcatel_base):
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


    #users
    #serviceport
    #servicevlan
    #port_profiles = relationship('PortProfile', backref='Box', lazy='dynamic')
    #port_profile_details = relationship('PortProfile', backref='port_profiles', lazy='dynamic')
    #vlans = relationship('Vlan', backref='Box', lazy='dynamic')
    #vlan_details = relationship('Vlan', backref='vlans', lazy='dynamic')
    #vlan_interfaces = relationship('VlanInterface', backref='Box', lazy='dynamic')
    #routes = relationship('Route', backref='Box', lazy='dynamic')
    #srvcs = relationship('Srvc', backref='Box', lazy='dynamic')

    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    version = Column(String(64), nullable=False)
    welcome_banner = Column(String)
    login_banner = Column(String)
    software_version = Column(String(64), nullable=False, default="R5.5.02")
    network_protocol = Column(Enum('telnet', 'ssh'), default='telnet')
    network_port = Column(Integer(), default=None)
    network_address = Column(String(), default=None)
    #uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid1()))
    description = Column(String())
    hostname = Column(String(64))
    mgmt_address = Column(String(32))
    default_gateway = Column(String(32), default='0.0.0.0')
    net_mask = Column(String(32), default='255.255.255.0')
    contact_person = Column(String(), default=None, nullable=True)
    isam_id = Column(String(), default=None, nullable=True)
    isam_location = Column(String(), default=None, nullable=True)


    def __repr__(self):
        return "<AlcatelBox(vendor='%s', model='%s', credentials='%s' and subracks='%s')>" %\
               (self.vendor, self.model, self.credentials, self.subrack)

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_fields()

    def check_credentials(self, username, password):
        for credential in self.credentials:
            if credential.username == username and credential.password == password:
                return True
        return False
