from experimental.db_models.config_models import *
from .service_vlan_models import AlcatelServiceVlan

@add_serviceportschema
class AlcatelServicePort(alcatel_base):
    __tablename__ = 'alcatelserviceport'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    service_vlans = relationship('AlcatelServiceVlan', backref='AlcatelServicePort')
    box_id = Column(Integer, ForeignKey('alcatelbox.id'))
    port_id = Column(Integer, ForeignKey('alcatelport.id'), nullable=True)
    cpe_port_id = Column(Integer, ForeignKey('alcatelcpeport.id'), nullable=True)
    ont_port_id = Column(Integer, ForeignKey('alcatelontport.id'), nullable=True)
    connected_id = Column(Integer(), nullable=True) # outdated but still in use
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
        self.set_fields()
        self.set_subcomponents()


    def set_fields(self):
        self.pvc = True
        self.admin_state = "down"
        self.operational_state = "down"
        if self.connected_type == 'port':
            self.connected_id = self.port_id
        elif self.connected_type == 'ont':
            self.connected_id = self.ont_port_id
        elif self.connected_type == 'cpe':
            self.connected_id = self.cpe_port_id

    def set_subcomponents(self):
        service_vlans = []
        for x in (2620, 3320):
            svlan = AlcatelServiceVlan(name=str(x), vlan_id=x, box_id=self.box_id)
            service_vlans.append(svlan)
        self.service_vlans = service_vlans
        return