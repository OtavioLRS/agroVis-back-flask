from flask import Blueprint

from .logic import getNotes, addNote


# Blueprint - Dados das anotações
anotacao_bp = Blueprint('anotacao_bp', __name__)


# Retorna todas as anotações
@anotacao_bp.route('/anotacoes', methods=['GET'])
def get_notes():
    return getNotes()


# Adiciona uma anotação
@anotacao_bp.route('/anotacoes', methods=['POST'])
def add_note():
    return addNote()
