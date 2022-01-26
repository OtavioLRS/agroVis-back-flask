from flask import json, request
from flask.helpers import make_response
import sqlalchemy
from sqlalchemy.sql import func, and_

from .models import ExportacaoAux
from application import db


# Recupera dados auxiliares para preencher o HorizonChart
def getHorizonAuxData():
    data = request.get_json()

    query = db.session.query(
        ExportacaoAux.CO_ANO.label("CO_ANO"),
        ExportacaoAux.CO_MES.label("CO_MES"),
        ExportacaoAux.SH4.label("SH4"),
        ExportacaoAux.NO_SH4_POR.label("NO_SH4_POR"),
        sqlalchemy.cast(func.sum(ExportacaoAux.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(ExportacaoAux.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
        func.count().label("NUM_REGS"),
    ).filter(
        and_(
            ExportacaoAux.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            func.date(
                ExportacaoAux.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(ExportacaoAux.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
        )
    ).group_by(
        ExportacaoAux.SH4,
        ExportacaoAux.CO_ANO,
        ExportacaoAux.CO_MES,
    )

    response = ExportacaoAux.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})