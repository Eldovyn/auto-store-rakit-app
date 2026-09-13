from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    CASCADE,
    IntField,
    FloatField,
)
from .player import PlayerModel


class QrisModel(Document):
    unique_code = StringField(required=True)
    amount = IntField(required=True)
    created_at = FloatField(required=True)
    message_id = IntField(required=False)
    player = ReferenceField(
        PlayerModel, required=True, reverse_delete_rule=CASCADE, unique=True
    )
    meta = {"collection": "qris"}
