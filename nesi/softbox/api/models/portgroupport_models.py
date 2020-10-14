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
    type = db.Column(db.Enum('ISDN', 'PSTN'), default='ISDN')

    #isdn
    enable = db.Column(db.Boolean(), default=False)
    register_as_global = db.Column(db.Boolean, default=None)
    register_default_number_only = db.Column(db.Boolean, default=None)
    layer_1_permanently_activated = db.Column(db.Boolean, default=None)
    sip_profile = db.Column(db.String(), default=None)
    proxy_registrar_profile = db.Column(db.String(), default=None)
    codec_sdp_profile = db.Column(db.String(), default=None)
    isdnba_profile = db.Column(db.String(), default=None)

    #pstn
    pay_phone = db.Column(db.Boolean(), default= None)
    pstn_profile = db.Column(db.String(), default=None)
    enterprise_profile = db.Column(db.String(), default=None)
