from nesi.softbox.api import db


class PortGroupPort(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    operational_state = db.Column(db.Enum('1', '0'), default='0')  # 0 => down, 1 => up
    admin_state = db.Column(db.Enum('1', '0'), default='0')
    description = db.Column(db.String(), default='')
    label1 = db.Column(db.String(), default='""')
    label2 = db.Column(db.String(), default='""')
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
