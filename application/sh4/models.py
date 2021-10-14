from application import db
from application.serializer import Serializer


class SH4(db.Model, Serializer):
    __tablename__ = 'sh4'
    CO_SH4 = db.Column(
        db.Integer,
        primary_key=True,
        index=True
    )

    NO_SH4_POR = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )

    def serialize(self):
        return super().serialize()
