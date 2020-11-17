from experimental.db_models.base_models import *
from .credentials_models import HuaweiCredentials


class HuaweiBox(huawei_base):
    __tablename__ = 'huaweibox'
    id = Column(Integer(), primary_key=True)
    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)
    credentials = relationship("HuaweiCredentials", backref="HuaweiBox")

    def __repr__(self):
        return "<HuaweiBox(vendor='%s', model='%s')>" % (self.vendor, self.model)
