from flask import json, request, jsonify
from flask.helpers import make_response
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Usuario
from application import db


# Valida um login
def loginUser():
    data = request.get_json()

    if data['email'] and data['password']:
        user = Usuario.query.filter_by(email=data['email']).first()

        if(not user):
            return make_response(jsonify({'msg': 'Usuário não cadastrado!'}), 400)

        if(user.check_password(data['password'])):
            user = user.serialize()
            user.pop('password', None)
            return make_response(jsonify(user), 200)

        else:
            return make_response(jsonify({'msg': 'Senha incorreta!'}), 400)

    else:
        return make_response(jsonify({'msg': 'Dados inválidas!'}), 400)


# Cria um usuario
def createUser():
    data = request.get_json()

    if data['email'] and data['password'] and data['name']:
        user_exists = Usuario.query.filter_by(email=data['email']).first()

        if(user_exists):
            return make_response(jsonify({'msg': 'Email já cadastrado!'}), 400)

        else:
            new_user = Usuario(email=data['email'], name=data['name'])
            new_user.set_password(data['password'])

        try:
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'result': {'email': data['email'], 'name': data['name']}}), 200)

        except:
            return jsonify({'msg': 'Erro no cadastro!'})

    else:
        return make_response(jsonify({'msg': 'Dados inválidas!'}), 400)
