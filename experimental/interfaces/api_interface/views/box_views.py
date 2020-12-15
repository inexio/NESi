from experimental.interfaces.api_interface.views.config_views import app, PREFIX, flask, json, exceptions, get_interface
from experimental.interfaces.api_interface.schemas.boxen_schemas import BoxenSchema

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
    INTERFACE = get_interface()
    boxen = INTERFACE.get_box(multiple=True)
    response = {
        'members': boxen,
        'count': len(boxen)
    }

    schema = BoxenSchema()
    response = schema.jsonify(response), 200
    INTERFACE.close_session()
    return response


@app.route(PREFIX + '/boxen/<id>', methods=['GET'])
def show_box(id):
    INTERFACE = get_interface()
    box = INTERFACE.get_box(id)

    if not box:
        raise exceptions.SoftboxenError()

    schema = box.Schema()
    response = schema.jsonify(box), 200
    INTERFACE.close_session()
    return response

@app.route(PREFIX + '/boxen', methods=['POST'])
def new_box():
    INTERFACE = get_interface()
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
    schema = box.Schema()
    response = schema.jsonify(box), 200
    INTERFACE.close_session()
    return response
