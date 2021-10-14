from flask import json

from .models import Cidade


# Recupera todas as cidades
def getCities():
    result = Cidade.query.all()

    return json.dumps(Cidade.serialize_list(result))
