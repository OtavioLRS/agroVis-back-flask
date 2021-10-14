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
        PRODUCTS=data["filter"]["products"],
        CITIES=data["filter"]["cities"],
        BEGIN_PERIOD=data["filter"]["beginPeriod"],
        END_PERIOD=data["filter"]["endPeriod"],
        SORT_VALUE=data["filter"]["sortValue"],
        MAP_SH4=data["map"]["sh4"],
        NUM_CLASS=data["map"]["numClasses"],
        TITLE=data["note"]["title"],
        TEXTO=data["note"]["text"],
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
