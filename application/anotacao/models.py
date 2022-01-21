from application import db
from application.serializer import Serializer


class Anotacao(db.Model, Serializer):
    __tablename__ = 'anotacao'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    FILTER_PRODUCTS = db.Column(db.Text)
    FILTER_CITIES = db.Column(db.Text)
    FILTER_COUNTRIES = db.Column(db.Text)
    FILTER_CONTINENTS = db.Column(db.Text)
    FILTER_SORT_VALUE = db.Column(db.Text)
    FILTER_MAP_DIVISION = db.Column(db.Text)
    FILTER_BEGIN_PERIOD = db.Column(db.DateTime)
    FILTER_END_PERIOD = db.Column(db.DateTime)

    MAP_SH4 = db.Column(db.Integer)
    MAP_NUM_CLASSES = db.Column(db.Integer)
    MUNDI_NUM_CLASSES = db.Column(db.Integer)

    HORIZON_OVERLAP = db.Column(db.Integer)
    HORIZON_SCALE = db.Column(db.Text)
    HORIZON_TYPE = db.Column(db.Text)
    HORIZON_ORDER = db.Column(db.Text)

    TITLE = db.Column(db.Text)
    TEXTO = db.Column(db.Text)
    REGISTER_DATE = db.Column(db.DateTime)

    def serialize(self):
        return super().serialize()
