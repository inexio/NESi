from experimental.db_models.base_models import *


class AlcatelCredentials(alcatel_base):
    __tablename__ = 'alcatelcredentials'
    id = Column(Integer(), primary_key=True)
    username = Column(String(64), nullable=True)
    password = Column(String(32), nullable=True)
    alcatel_box_id = Column(Integer, ForeignKey('alcatelbox.id'))

    def __repr__(self):
        return "<Credentials(username='%s', pw='%s')>" % (self.username, self.password)

