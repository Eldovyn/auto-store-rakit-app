from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    FloatField,
    DynamicField,
    IntField,
    CASCADE,
)
from .player import PlayerModel


class HistoryModel(Document):
    history_id = IntField(required=True, unique=True)
    code = StringField(required=True)
    category = StringField(required=True)
    item = DynamicField(required=True)
    payment = StringField(required=True)
    price = IntField(required=True)
    total_price = IntField(required=True)
    created_at = FloatField(required=True)
    message_id = IntField(required=False)
    player = ReferenceField(PlayerModel, required=True, reverse_delete_rule=CASCADE)
    meta = {"collection": "history"}
