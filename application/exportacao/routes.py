from flask import Blueprint

from .logic import getMapData, getMundiData, getHorizonData, getHorizonAuxData, getModalData


# Blueprint - Dados das anotações
exportacao_bp = Blueprint('exportacao_bp', __name__)


@exportacao_bp.route('/exportacao/mapa', methods=['POST'])
def get_map_data():
    return getMapData()


@exportacao_bp.route('/exportacao/mundi', methods=['POST'])
def get_mundi_data():
    return getMundiData()


@exportacao_bp.route('/exportacao/horizon', methods=['POST'])
def get_horizon_data():
    return getHorizonData()


@exportacao_bp.route('/exportacao/horizon/aux', methods=['POST'])
def get_horizon_aux_data():
    return getHorizonAuxData()


@exportacao_bp.route('/exportacao/modal', methods=['POST'])
def get_modal_data():
    return getModalData()
