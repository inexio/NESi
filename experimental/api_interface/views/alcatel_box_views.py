
from flask import Flask
import flask
import json
from nesi.softbox.api import config
from experimental.db_interfaces.alcatel_interface import AlcatelInterface
from nesi import exceptions
from ..schemas.box_schemas import *


app = Flask(__name__)
app.config.from_object(config.DefaultConfig)
PREFIX = '/nesi/v1'
INTERFACE = AlcatelInterface(False)


@app.route(PREFIX + '/')
def show_root():
    response = {
        'description': 'Network Equipment Simulator REST API ',
        'boxen': {
            '_links': {
                'self': flask.url_for('show_boxen')
            }
        }
    }

    return json.dumps(response), 200


@app.route(PREFIX + '/boxen', methods=['GET'])
def show_boxen():
    boxen = INTERFACE.get_box(multiple=True)
    response = {
        'members': boxen,
        'count': len(boxen)
    }

    schema = BoxenSchema()
    INTERFACE.close_session()
    return schema.jsonify(response), 200


@app.route(PREFIX + '/boxen/<id>', methods=['GET'])
def show_box(id):
    box = INTERFACE.get_box(id)

    if not box:
        raise exceptions.SoftboxenError()

    schema = BoxSchema()
    INTERFACE.close_session()
    return schema.jsonify(box), 200

@app.route(PREFIX + '/boxen', methods=['POST'])
def new_box():
    req = flask.request.json

    box_data = req.copy()

    # Additional components have to be wiped from box_data as a box can otherwise not be created
    components = ('credentials', 'subracks', 'cards', 'ports', 'onts', 'ont_ports', 'cpes', 'cpe_ports', 'vlans',
                  'port_profiles', 'routes')
    for component in components:
        if component in req:
            del box_data[component]

    box = INTERFACE.box(**box_data)
    INTERFACE.store(box)
    schema = BoxSchema()
    response = schema.jsonify(box), 200
    INTERFACE.close_session()
    return response
