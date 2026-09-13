from mongoengine import Document, StringField, IntField, FloatField


class PlayerModel(Document):
    discord_id = IntField(required=True)
    growid = StringField(required=True)
    created_at = FloatField(required=True)
    updated_at = FloatField(required=True)
    world_lock = IntField(default=0)
    total_buy = IntField(default=0)
    meta = {"collection": "player"}
