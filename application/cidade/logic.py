from flask import json
from flask.helpers import make_response

from .models import Cidade


# Recupera todas as cidades
def getCities():
    result = Cidade.query.all()

    return make_response(json.dumps(Cidade.serialize_list(result)), 200, {"Content-Type": "application/json"})
