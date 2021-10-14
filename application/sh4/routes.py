from flask import Blueprint

from .logic import getProducts


# Blueprint - Dados dos produtos
sh4_bp = Blueprint('sh4_bp', __name__)


# Retorna todos os produtos (SH4s)
@sh4_bp.route('/produtos', methods=['GET'])
def get_products():
    return getProducts()
