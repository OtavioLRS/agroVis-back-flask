from application import db
from application.serializer import Serializer


class Exportacao(db.Model, Serializer):
    __tablename__ = 'exportacao_teste'
    KEY = db.Column(db.String(21), primary_key=True,
                    index=True)
    CO_DATA = db.Column(db.DateTime, index=True)
    CO_ANO = db.Column(db.Integer, index=True)
    CO_MES = db.Column(db.Integer, index=True)
    CO_MUN = db.Column(db.Text, index=True)
    NO_MUN_MIN = db.Column(db.Text)
    CO_PAIS = db.Column(db.Integer, index=True)
    NO_PAIS = db.Column(db.Text)
    CO_BLOCO = db.Column(db.Integer, index=True)
    NO_BLOCO = db.Column(db.Text)
    SH4 = db.Column(db.Integer, index=True)
    NO_SH4_POR = db.Column(db.Text)
    KG_LIQUIDO = db.Column(db.BigInteger)
    VL_FOB = db.Column(db.BigInteger)

    def serialize(self):
        return super().serialize()
