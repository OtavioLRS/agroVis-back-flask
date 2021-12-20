from flask import Blueprint

from .logic import getMapData, getHorizonData, getHorizonAuxData, getModalData, getMundiDataContinent, getMundiDataCountry


# Blueprint - Dados das anotações
exportacao_bp = Blueprint('exportacao_bp', __name__)


@exportacao_bp.route('/exportacao/mapa', methods=['POST'])
def get_map_data():
    return getMapData()


@exportacao_bp.route('/exportacao/mundi/continente', methods=['POST'])
def get_mundi_data_continent():
    return getMundiDataContinent()


@exportacao_bp.route('/exportacao/mundi/pais', methods=['POST'])
def get_mundi_data_country():
    return getMundiDataCountry()


@exportacao_bp.route('/exportacao/horizon', methods=['POST'])
def get_horizon_data():
    return getHorizonData()


@exportacao_bp.route('/exportacao/horizon/aux', methods=['POST'])
def get_horizon_aux_data():
    return getHorizonAuxData()


@exportacao_bp.route('/exportacao/horizon/modal', methods=['POST'])
def get_modal_data():
    return getModalData()
