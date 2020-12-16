from experimental.db_models.config_models import *


@add_serviceportschema
class AlcatelServicePort(alcatel_base):
    __tablename__ = 'alcatelserviceport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    connected_id = Column(Integer(), nullable=False)
    connected_type = Column(Enum('port', 'ont', 'cpe'), nullable=False)

    # Alcatel data
    pvid = Column(Integer(), default=None, nullable=True)
    max_unicast_mac = Column(Integer(), default=None, nullable=True)
    qos_profile_id = Column(Integer(), default=None, nullable=True)
    pvc = Column(Boolean(), default=False)
    admin_state = Column(Enum('down', 'up'), default='down')
    operational_state = Column(Enum('down', 'up'), default='down')

    def __repr__(self):
        return "<AlcatelServicePort(id='%s', name='%s', box_id='%s', connected_type=%s' and connected_id='%s')>" %\
               (self.id, self.name, self.box_id, self.connected_type, self.connected_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
