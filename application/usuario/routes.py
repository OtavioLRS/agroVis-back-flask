from flask import Blueprint, make_response
from flask import current_app as app
from flask.json import jsonify
# from application import

usuario_bp = Blueprint(
    'usuario_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@usuario_bp.route('/', methods=['GET'])
def users():
    head = {"Content-Type": "application/json"}
    return make_response(jsonify({'sim': 'a'}), 200, head)
