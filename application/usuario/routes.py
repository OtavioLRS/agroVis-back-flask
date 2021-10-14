from flask import Blueprint

from .logic import createUser, loginUser


usuario_bp = Blueprint('usuario_bp', __name__)


# Criação de usuário
@usuario_bp.route('/user/create', methods=['POST'])
def create_user():
    return createUser()


# Validação de login
@usuario_bp.route('/user/login', methods=['POST'])
def login_user():
    return loginUser()
