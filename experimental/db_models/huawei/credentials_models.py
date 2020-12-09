from experimental.db_models.config_models import *


class HuaweiCredentials(huawei_base):
    __tablename__ = 'huaweicredentials'
    id = Column(Integer(), primary_key=True)
    username = Column(String(64), nullable=True)
    password = Column(String(32), nullable=True)
    huawei_box_id = Column(Integer, ForeignKey('huaweibox.id'))

    def __repr__(self):
        return "<Credentials(username='%s', pw='%s')>" % (self.username, self.password)
