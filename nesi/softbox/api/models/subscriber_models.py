# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
# - Philipp-Noah Groß <https://github.com/pngross>
#
# License: https://github.com/inexio/NESi/LICENSE.rst<

from nesi.softbox.api import db


class Subscriber(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    box_id = db.Column(db.Integer, db.ForeignKey('box.id'))
    portgroupport_id = db.Column(db.Integer(), db.ForeignKey('port_group_port.id'))

    number = db.Column(db.Integer(), nullable=False, unique=True)
    address = db.Column(db.String(), default='')
    registration_state = db.Column(
        db.Enum('Registered', 'Registering', 'RegisteringWith-Cred',
                'DeRegInRegistering', 'DeRegistering', 'Reregistering',
                'Unregistered'), default='Registered')
    autorisation_user_name = db.Column(db.String(), default='')
    autorisation_password = db.Column(db.String(), default='')
    display_name = db.Column(db.String(), default='')
    privacy = db.Column(db.String(), default='None')

