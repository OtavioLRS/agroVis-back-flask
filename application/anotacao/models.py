from application import db
from application.serializer import Serializer


class Anotacao(db.Model, Serializer):
    __tablename__ = 'anotacao'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PRODUCTS = db.Column(db.Text)
    CITIES = db.Column(db.Text)
    BEGIN_PERIOD = db.Column(db.DateTime)
    END_PERIOD = db.Column(db.DateTime)
    SORT_VALUE = db.Column(db.Text)
    MAP_SH4 = db.Column(db.Integer)
    NUM_CLASS = db.Column(db.Integer)
    TITLE = db.Column(db.Text)
    TEXTO = db.Column(db.Text)
    REGISTER_DATE = db.Column(db.DateTime)

    def serialize(self):
        return super().serialize()
