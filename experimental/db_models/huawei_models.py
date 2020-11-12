from .base_models import *
from .base_base_models import Credentials


class HuaweiBox(huawei_base):
    __tablename__ = 'huaweibox'
    id = Column(Integer(), primary_key=True)
    vendor = Column(String(64), nullable=False)
    model = Column(String(64), nullable=False)

    def __repr__(self):
        return "<HuaweiBox(vendor='%s', model='%s')>" % (self.vendor, self.model)
