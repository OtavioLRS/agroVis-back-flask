from flask import json, request
from flask.helpers import make_response
import sqlalchemy
from sqlalchemy.sql import func, and_, or_

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
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
        )
    ).group_by(Exportacao.CO_MUN)    
    query = query.order_by(func.sum(Exportacao.VL_FOB).asc()) if data["filter"]["sortValue"] == "VL_FOB" else query.order_by(func.sum(Exportacao.KG_LIQUIDO).asc())

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
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
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
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.VL_FOB != 0,
            Exportacao.CO_MUN != 0000000,

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
        )
    ).group_by(
        Exportacao.CO_PAIS,
    ).order_by(func.sum(Exportacao.VL_FOB).asc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})


# Recupera dados utilizados para prencher o modal do mapa
def getMapModalData() :
    data = request.get_json()

    # Primeira query, identificar a ordem dos SH4s
    firstQuery = db.session.query(
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
            Exportacao.CO_MUN != 0000000,

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
        )
    ).group_by(Exportacao.SH4)
    firstQuery = firstQuery.order_by(func.sum(Exportacao.VL_FOB).desc()) if data["filter"]["sortValue"] == "VL_FOB" else firstQuery.order_by(func.sum(Exportacao.KG_LIQUIDO).desc())
    firstResults = Exportacao.serialize_rowlist(db.session.execute(firstQuery))

    finalResults = []
    # Queries parciais para cada SH4
    for row in firstResults:
        # DIVISÃO POR PAIS
        if data["filter"]["mapDivision"] == "country":
            query = db.session.query(
                Exportacao.CO_MUN.label("CO_MUN"),
                Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
                Exportacao.CO_PAIS.label("CO_PAIS"),
                Exportacao.NO_PAIS.label("NO_PAIS"),
                Exportacao.SH4.label("SH4"),
                Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
                sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                            sqlalchemy.BigInteger).label("KG_LIQUIDO"),
                sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                            sqlalchemy.BigInteger).label("VL_FOB"),
                (100 * (func.sum(Exportacao.VL_FOB) / (row["VL_FOB"]))).label("VL_FOB_PERCENT"),
                (100 * (func.sum(Exportacao.KG_LIQUIDO) / (row["KG_LIQUIDO"]))).label("KG_LIQUIDO_PERCENT"),
            ).filter(
                and_(
                    Exportacao.CO_MUN.in_(
                        data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
                    Exportacao.SH4 == row["SH4"],
                    func.date(Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
                    func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
                    Exportacao.CO_MUN != 0000000,
                    Exportacao.CO_PAIS.in_(data["filter"]["countries"]) if data["filter"]["countries"] != [] else sqlalchemy.true()
                )
            )
        
        # DIVISÃO POR CONTINENTE
        else: 
            query = db.session.query(
                Exportacao.CO_MUN.label("CO_MUN"),
                Exportacao.NO_MUN_MIN.label("NO_MUN_MIN"),
                Exportacao.CO_BLOCO.label("CO_BLOCO"),
                Exportacao.NO_BLOCO.label("NO_BLOCO"),
                Exportacao.SH4.label("SH4"),
                Exportacao.NO_SH4_POR.label("NO_SH4_POR"),
                sqlalchemy.cast(func.sum(Exportacao.KG_LIQUIDO),
                            sqlalchemy.BigInteger).label("KG_LIQUIDO"),
                sqlalchemy.cast(func.sum(Exportacao.VL_FOB),
                            sqlalchemy.BigInteger).label("VL_FOB"),
                (100 * (func.sum(Exportacao.VL_FOB) / (row["VL_FOB"]))).label("VL_FOB_PERCENT"),
                (100 * (func.sum(Exportacao.KG_LIQUIDO) / (row["KG_LIQUIDO"]))).label("KG_LIQUIDO_PERCENT"),
            ).filter(
                and_(
                    Exportacao.CO_MUN.in_(
                        data["filter"]["cities"]) if data["filter"]["cities"] != [] else sqlalchemy.true(),
                    Exportacao.SH4 == row["SH4"],
                    func.date(Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
                    func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
                    Exportacao.CO_MUN != 0000000,
                    Exportacao.CO_BLOCO.in_(data["filter"]["continents"]) if data["filter"]["continents"] != [] else sqlalchemy.true()
                )
            )

        aggregation = ""
        if data["filter"]["aggregationType"] == "mundi":
            query = query.group_by(Exportacao.SH4, Exportacao.CO_MUN)
            aggregation = "NO_MUN_MIN"
            # print('clicou no mundi, agrupa por cidade')
        elif data["filter"]["mapDivision"] == "country": 
            query = query.group_by(Exportacao.SH4, Exportacao.CO_PAIS)
            aggregation = "NO_PAIS"
            # print('clicou no mapa, agrupa por pais')
        else:
            query = query.group_by(Exportacao.SH4, Exportacao.CO_BLOCO)
            aggregation = "NO_BLOCO"
            # print('clicou no mapa, agrupa por continente')

        query = query.order_by(func.sum(Exportacao.VL_FOB).desc()) if data["filter"]["sortValue"] == "VL_FOB" else query.order_by(func.sum(Exportacao.KG_LIQUIDO).desc())

        parcialResults = Exportacao.serialize_rowlist(db.session.execute(query))
        finalResults.append({
            "SH4": row["SH4"], 
            "SH4_NAME": row["NO_SH4_POR"], 
            "SUM": row["VL_FOB"] if data["filter"]["sortValue"] == "VL_FOB" else row["KG_LIQUIDO"], 
            "TYPE": data["filter"]["sortValue"],
            "AGGREGATION": aggregation, 
            "DATA": parcialResults})

    return make_response(json.dumps(finalResults), 200, {"Content-Type": "application/json"})


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
            func.date(
                Exportacao.CO_DATA) >= data["filter"]["beginPeriod"]+"-01",
            func.date(Exportacao.CO_DATA) <= data["filter"]["endPeriod"]+"-30",
            Exportacao.CO_MUN != 0000000,

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
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

            (Exportacao.CO_PAIS.in_(data["filter"]["countries"])
             if data["filter"]["countries"] != [] else sqlalchemy.true())

            if data["filter"]["mapDivision"] == 'country' else

            (Exportacao.CO_BLOCO.in_(data["filter"]["continents"])
             if data["filter"]["continents"] != [] else sqlalchemy.true())
        )
    ).group_by(
        Exportacao.CO_MUN,
    ).order_by(func.sum(Exportacao.VL_FOB).desc())

    response = Exportacao.serialize_rowlist(db.session.execute(query))

    return make_response(json.dumps(response), 200, {"Content-Type": "application/json"})
