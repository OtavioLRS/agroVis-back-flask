from flask import Blueprint

from .logic import getHorizonAuxData


# Blueprint - Dados das anotações
exportacao_aux_bp = Blueprint('exportacao_aux_bp', __name__)


@exportacao_aux_bp.route('/exportacao/horizon/aux', methods=['POST'])
def get_horizon_aux_data():
    return getHorizonAuxData()
