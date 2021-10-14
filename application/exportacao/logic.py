from flask import json, request
from flask.helpers import make_response
import sqlalchemy
from sqlalchemy.sql import func, and_, or_, asc, desc, cast

from sqlalchemy.sql.sqltypes import BigInteger, Float, Integer, Text

from .models import Exportacao
from application import db


# Recupera dados utilizados para prencher o mapa
def getMapData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_MUN.label("CO_MUN"),
        Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        func.sum(Exportacao.KG_LIQUIDO, type=Integer).label("KG_LIQUIDO"),
        func.sum(Exportacao.VL_FOB, type=Integer).label("VL_FOB"),
        func.count().label("NUM_REGS")
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.CO_MUN,
        Exportacao.SH4,
    ).order_by(
        asc(Exportacao.VL_FOB)
    )

    response = Exportacao.serialize_rowlist(
        db.session.execute(query), cast_to_int=["VL_FOB", "KG_LIQUIDO"])

    return json.dumps(response)


# Recupera dados utilizados para preencher o HorizonChart
def getHorizonData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_ANO.label("CO_ANO"),
        Exportacao.CO_MES.label("CO_MES"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        func.sum(Exportacao.KG_LIQUIDO, type=Integer).label("KG_LIQUIDO"),
        func.sum(Exportacao.VL_FOB, type=Integer).label("VL_FOB"),
        func.count().label("NUM_REGS"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.SH4,
        Exportacao.CO_ANO,
        Exportacao.CO_MES,
    )

    response = Exportacao.serialize_rowlist(
        db.session.execute(query), cast_to_int=["VL_FOB", "KG_LIQUIDO"])

    return json.dumps(response)


# Recupera dados auxiliares para preencher o HorizonChart
def getHorizonAuxData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_ANO.label("CO_ANO"),
        Exportacao.CO_MES.label("CO_MES"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        func.sum(Exportacao.KG_LIQUIDO, type=Integer).label("KG_LIQUIDO"),
        func.sum(Exportacao.VL_FOB, type=Integer).label("VL_FOB"),
        func.count().label("NUM_REGS"),
    ).filter(
        and_(
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.CO_MUN == 0000000,
        )
    ).group_by(
        Exportacao.SH4,
        Exportacao.CO_ANO,
        Exportacao.CO_MES,
    )

    response = Exportacao.serialize_rowlist(
        db.session.execute(query), cast_to_int=["VL_FOB", "KG_LIQUIDO"])

    return json.dumps(response)


# Recupera dados para preencher o modal de um SH4
def getModalData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_MUN.label("CO_MUN"),
        Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        func.sum(Exportacao.KG_LIQUIDO, type=Integer).label("KG_LIQUIDO"),
        func.sum(Exportacao.VL_FOB, type=Integer).label("VL_FOB"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.CO_MUN,
    ).order_by(
        desc(Exportacao.VL_FOB)
    )

    response = Exportacao.serialize_rowlist(
        db.session.execute(query), cast_to_int=["VL_FOB", "KG_LIQUIDO"])

    return json.dumps(response)
