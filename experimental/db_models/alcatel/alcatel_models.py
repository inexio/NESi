from experimental.db_models.base_models import *
from .credentials_models import AlcatelCredentials
import json
import uuid


class AlcatelBox(alcatel_base):
    __tablename__ = 'alcatelbox'

    id = Column(Integer(), primary_key=True)
    subrack = relationship("AlcatelSubrack", backref="AlcatelBox")
    credentials = relationship("AlcatelCredentials", backref="AlcatelBox")

    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_fields()


class AlcatelSubrack(alcatel_base):
    __tablename__ = 'alcatelsubrack'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64), nullable=False)
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))

    def __repr__(self):
        return "<Subrack(name='%s', box_id='%s')>" % (self.name, self.box_id)

