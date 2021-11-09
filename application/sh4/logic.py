from flask import json
from flask.helpers import make_response

from .models import SH4


# Recupera todos os sh4s
def getProducts():
    result = SH4.query.all()

    return make_response(json.dumps(SH4.serialize_list(result)), 200, {"Content-Type": "application/json"})
