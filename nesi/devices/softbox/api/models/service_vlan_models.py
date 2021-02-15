from nesi.devices.softbox.api import db


class ServiceVlan(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    service_port_id = db.Column(db.Integer, db.ForeignKey('service_port.id'))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    vlan_id = db.Column(db.Integer, db.ForeignKey('vlan.id'), nullable=False)
    qos_profile_id = db.Column(db.Integer(), default=None)
    l2fwder_vlan = db.Column(db.Integer(), default=None)
    scope = db.Column(db.Enum('local'), default='local')
    tag = db.Column(db.Enum('single-tagged', 'untagged'), default='single-tagged')

    mode = db.Column(db.Enum('atm', 'ptm'), default='ptm')
