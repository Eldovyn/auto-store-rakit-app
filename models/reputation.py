from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    FloatField,
    BinaryField,
    IntField,
    CASCADE,
)
from .player import PlayerModel


class ReputationModel(Document):
    reputation_id = IntField(required=True, unique=True)
    message = StringField(required=True)
    star = StringField(required=True)
    created_at = FloatField(required=True)
    image = BinaryField(required=False)
    player = ReferenceField(PlayerModel, required=True, reverse_delete_rule=CASCADE)
    message_id_user = IntField(required=False)
    message_id_bot = IntField(required=False)
    meta = {"collection": "reputation"}
