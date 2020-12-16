from nesi.softbox.api import config
from experimental.interfaces.db_interfaces.alcatel_interface import AlcatelInterface
from flask import Flask
from nesi import exceptions
import flask
import json

app = Flask(__name__)
app.config.from_object(config.DefaultConfig)
PREFIX = '/nesi/v1'


def get_interface():
    return AlcatelInterface(False)

from .subrack_views import *
from .box_views import *
from .card_views import *
from .port_views import *
from .mgmt_card_views import *
from .mgmt_port_views import *



