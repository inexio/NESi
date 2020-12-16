from experimental.db_models.config_models import *
from experimental.db_models.alcatel.user_models import AlcatelUser


@add_credentialschema
class AlcatelCredentials(alcatel_base):
    __tablename__ = 'alcatelcredentials'
    id = Column(Integer(), primary_key=True)
    username = Column(String(64), nullable=True)
    password = Column(String(32), nullable=True)
    user = relationship('AlcatelUser', backref='AlcatelCredentials')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))

    def __repr__(self):
        return "<Credentials(username='%s', pw='%s')>" % (self.username, self.password)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_subcomponents()

    def set_subcomponents(self):
        self.user = [AlcatelUser(name='admin', box_id=self.box_id)]

