from flask import json

from .models import SH4_NCM


# Recupera as conversões de um SH4
def getConversion(sh4):
    print(sh4)
    result = SH4_NCM.query.filter_by(CO_SH4=sh4)

    return json.dumps(SH4_NCM.serialize_list(result))
