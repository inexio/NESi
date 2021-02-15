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

import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import logging

from nesi.devices.softbox.api import config


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = False
app.logger.disabled = False

app.url_map.strict_slashes = False

app.config.from_object(config.DefaultConfig)

if 'NESI_CONFIG' in os.environ:
    app.config.from_envvar('NESI_CONFIG')

db = SQLAlchemy(app)
ma = Marshmallow(app)
