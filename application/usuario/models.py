from application import db
from application.serializer import Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model, Serializer):
    __tablename__ = 'usuario'
    index = db.Column(db.Integer, index=True)
    email = db.Column(db.String(150), primary_key=True, unique=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return super().serialize()
