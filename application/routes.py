from flask import Blueprint


home_bp = Blueprint('home_bp', __name__)

# Index
@home_bp.route('/', methods=['GET'])
def index():
    return "<h1>AgroVis-FCT => Backend - Flask</h1>"
