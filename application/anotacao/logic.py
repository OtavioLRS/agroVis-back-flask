from flask import json, request
from flask.helpers import make_response
import datetime

from .models import Anotacao
from application import db


# Recupera todas as anotações
def getNotes():
    result = Anotacao.query.all()

    return json.dumps(Anotacao.serialize_list(result))


# Adiciona uma anotação
def addNote():
    data = request.get_json()

    new_note = Anotacao(
        FILTER_PRODUCTS = data["filter"]["products"],
        FILTER_CITIES = data["filter"]["cities"],
        FILTER_COUNTRIES = data["filter"]["countries"],
        FILTER_CONTINENTS = data["filter"]["continents"],
        FILTER_SORT_VALUE = data["filter"]["sortValue"],
        FILTER_MAP_DIVISION = data["filter"]["mapDivision"],
        FILTER_BEGIN_PERIOD = data["filter"]["beginPeriod"],
        FILTER_END_PERIOD = data["filter"]["endPeriod"],

        MAP_SH4 = data["map"]["mapSh4"],
        MAP_NUM_CLASSES = data["map"]["mapNumClasses"],
        MUNDI_NUM_CLASSES = data["map"]["mundiNumClasses"],

        HORIZON_OVERLAP = data["horizon"]["overlap"],
        HORIZON_SCALE = data["horizon"]["horizonScale"],
        HORIZON_TYPE = data["horizon"]["horizonType"],
        HORIZON_ORDER = data["horizon"]["horizonOrder"],

        TITLE = data["note"]["title"],
        TEXTO = data["note"]["text"],

        REGISTER_DATE=datetime.datetime.now()
    )

    try:
        db.session.add(new_note)
        db.session.commit()

        response = json.jsonify({'msg': 'Anotação cadastrada!'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except:
        response = json.jsonify({'msg': 'Erro!'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
