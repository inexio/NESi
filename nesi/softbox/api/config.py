# This file is part of the NESi software.
#
# Copyright (c) 2020
# Original Software Design by Ilya Etingof <https://github.com/etingof>.
#
# Software adapted by inexio <https://github.com/inexio>.
# - Janis Groß <https://github.com/unkn0wn-user>
# - Philip Konrath <https://github.com/Connyko65>
# - Alexander Dincher <https://github.com/Dinker1996>
#
# License: https://github.com/inexio/NESi/LICENSE.rst


class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    DEBUG = False

    NESI_MGMT_LISTEN_IP = '127.0.0.1'
    NESI_MGMT_LISTEN_PORT = 5000
    NESI_MGMT_SSL_CERT = None
    NESI_MGMT_SSL_KEY = None
