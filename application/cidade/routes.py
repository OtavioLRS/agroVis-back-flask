from flask import Blueprint

from .logic import getCities


# Blueprint - Dados das cidades
cidade_bp = Blueprint('cidade_bp', __name__)


# Retorna todas as cidades
@cidade_bp.route('/cidades', methods=['GET'])
def get_cities():
    return getCities()
