from .base_models import *
from .base_base_models import Credentials
import json


class AlcatelBox(alcatel_base):
    __tablename__ = 'alcatelbox'

    id = Column(Integer(), primary_key=True)
    subrack = relationship("AlcatelSubrack", backref="AlcatelBox")
    credentials = relationship("Credentials", backref="AlcatelBox")

    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    welcome_banner = Column(String)
    login_banner = Column(String)

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

