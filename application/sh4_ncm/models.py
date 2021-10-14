from application import db
from application.serializer import Serializer


class SH4_NCM(db.Model, Serializer):
    __tablename__ = 'sh4_ncm'
    INDEX = db.Column(db.Integer, index=True, autoincrement=True)
    CO_SH4 = db.Column(db.Text, primary_key=True, index=True)
    NO_SH4_POR = db.Column(db.Text)
    CO_SH6 = db.Column(db.Text)
    NO_SH6_POR = db.Column(db.Text)
    CO_NCM = db.Column(db.Text, primary_key=True)
    NO_NCM_POR = db.Column(db.Text)

    def serialize(self):
        return super().serialize()
