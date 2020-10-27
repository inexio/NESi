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
    register_as_global = db.Column(db.Boolean, default=True)
    register_default_number_only = db.Column(db.Boolean, default=False)
    layer_1_permanently_activated = db.Column(db.Boolean, default=False)
    sip_profile = db.Column(db.String(), default='none')
    proxy_registrar_profile = db.Column(db.String(), default='none')
    codec_sdp_profile = db.Column(db.String(), default='none')
    isdnba_profile = db.Column(db.String(), default='none')

    #pstn
    pay_phone = db.Column(db.Boolean(), default=False)
    pstn_profile = db.Column(db.String(), default='none')
    enterprise_profile = db.Column(db.String(), default='none')
