from nesi.softbox.api import config
from experimental.db_interfaces.alcatel_interface import AlcatelInterface
from flask import Flask

app = Flask(__name__)
app.config.from_object(config.DefaultConfig)
PREFIX = '/nesi/v1'
INTERFACE = AlcatelInterface(False)

from .subrack_views import *
from .alcatel_box_views import *
