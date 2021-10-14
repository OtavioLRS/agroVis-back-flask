from application import db
from application.serializer import Serializer


class Cidade(db.Model, Serializer):
    __tablename__ = 'cidade'
    CO_MUN_GEO = db.Column(
        db.Integer,
        primary_key=True,
        index=True
    )

    NO_MUN = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=False
    )

    NO_MUN_MIN = db.Column(
        db.String(100),
        index=False,
        unique=False,
        nullable=False
    )

    SG_UF = db.Column(
        db.String(2),
        index=False,
        unique=False,
        nullable=False
    )

    def serialize(self):
        return super().serialize()
