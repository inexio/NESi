from experimental.db_models.config_models import *


class AlcatelServiceVlan(alcatel_base):
    __tablename__ = 'alcatelservicevlan'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    service_port_id = Column(Integer, ForeignKey('alcatelserviceport.id'))
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    card_id = Column(Integer, ForeignKey('alcatelcard.id'))
    vlan_id = Column(Integer, ForeignKey('alcatelvlan.id'), nullable=False)
    qos_profile_id = Column(Integer(), default=None)
    l2fwder_vlan = Column(Integer(), default=None)
    scope = Column(Enum('local'), default='local')
    tag = Column(Enum('single-tagged', 'untagged'), default='single-tagged')

    mode = Column(Enum('atm', 'ptm'), default='ptm')

    def __repr__(self):
        return "<AlcatelServiceVlan(id='%s', name='%s', box_id='%s', vlan_id=%s' and service_port_id='%s')>" %\
               (self.id, self.name, self.box_id, self.vlan_id, self.service_port_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
