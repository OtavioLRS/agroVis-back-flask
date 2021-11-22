from flask import json, request
from flask.helpers import make_response
import sqlalchemy
from sqlalchemy.sql import func, and_, or_, asc, desc
from sqlalchemy.sql.expression import cast

from sqlalchemy.sql.sqltypes import Integer

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
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            Exportacao.CO_BLOCO.in_(
                data["filter"]["continents"]) if data["filter"]["continents"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.CO_MUN,
        Exportacao.SH4,
    ).order_by(func.sum(Exportacao.VL_FOB).asc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados utilizados para prencher o mapa mundi por continente
def getMundiDataContinent():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_MUN.label("CO_MUN"),
        Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        Exportacao.CO_BLOCO.label("CO_BLOCO"),
        Exportacao.NO_BLOCO.label("NO_BLOCO"),
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            Exportacao.CO_BLOCO.in_(
                data["filter"]["continents"]) if data["filter"]["continents"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.CO_BLOCO,
    ).order_by(func.sum(Exportacao.VL_FOB).asc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados utilizados para prencher o mapa mundi por pais
def getMundiDataCountry():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_MUN.label("CO_MUN"),
        Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        Exportacao.CO_PAIS.label("CO_PAIS"),
        Exportacao.NO_PAIS.label("NO_PAIS"),
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            Exportacao.CO_BLOCO.in_(
                data["filter"]["continents"]) if data["filter"]["continents"] != [] else sqlalchemy.true(),
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,
        )
    ).group_by(
        Exportacao.CO_PAIS,
    ).order_by(func.sum(Exportacao.VL_FOB).asc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados utilizados para preencher o HorizonChart
def getHorizonData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_ANO.label("CO_ANO"),
        Exportacao.CO_MES.label("CO_MES"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
        func.count().label("NUM_REGS"),
    ).filter(
        and_(
            Exportacao.CO_MUN.in_(
                data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
            Exportacao.SH4.in_(
                data["filter"]["products"]) if data["filter"]["products"] != [] else sqlalchemy.true(),
            Exportacao.CO_BLOCO.in_(
                data["filter"]["continents"]) if data["filter"]["continents"] != [] else sqlalchemy.true(),
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

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados auxiliares para preencher o HorizonChart
def getHorizonAuxData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_ANO.label("CO_ANO"),
        Exportacao.CO_MES.label("CO_MES"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
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

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados para preencher o modal de um SH4
def getModalData():
    data = request.get_json()

    query = db.session.query(
        Exportacao.CO_MUN.label("CO_MUN"),
        Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
        Exportacao.SH4.label("SH4"),
        Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
        sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                        sqlalchemy.BigInteger).label("KG_LIQUIDO"),
        sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                        sqlalchemy.BigInteger).label("VL_FOB"),
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
    ).order_by(func.sum(Exportacao.VL_FOB).desc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})
