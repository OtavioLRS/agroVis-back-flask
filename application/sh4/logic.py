from flask import json

from .models import SH4


# Recupera todos os sh4s
def getProducts():
    result = SH4.query.all()

    return json.dumps(SH4.serialize_list(result))
