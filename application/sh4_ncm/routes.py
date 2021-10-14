from flask import Blueprint

from .logic import getConversion


# Blueprint - Dados das conversões
sh4_ncm_bp = Blueprint('sh4_ncm_bp', __name__)


# Retorna uma conversão
@sh4_ncm_bp.route('/codigos/<sh4>', methods=['GET'])
def get_conversion(sh4):
    return getConversion(sh4)
