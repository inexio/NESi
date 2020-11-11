from .base_models import *


class AlcatelBox(alcatel_base):
    __tablename__ = 'alcatelbox'

    id = Column(Integer(), primary_key=True)
    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    password = Column(Integer)
    subrack = relationship("AlcatelSubrack", back_populates="box")

    def __repr__(self):
        return "<AlcatelBox(vendor='%s', model='%s', pw='%s' and subracks='%s')>" % (self.vendor, self.model, self.password, self.subrack)

    def set_pw(self):
        self.password = 5

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_pw()

class AlcatelSubrack(alcatel_base):
    __tablename__ = 'alcatelsubrack'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64), nullable=False)
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    box = relationship("AlcatelBox", back_populates="subrack")

    def __repr__(self):
        return "<Subrack(name='%s', box_id='%s')>" % (self.name, self.box_id)