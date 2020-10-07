from nesi.softbox.api import db


class Subscriber(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))

    number = db.Column(db.Integer(), nullable=False, unique=True)
    type = db.Column(db.Enum('unit', 'port'), default='port')
    address = db.Column(db.String(), default='')
    registration_state = db.Column(db.Enum('registered'), default='registered')

