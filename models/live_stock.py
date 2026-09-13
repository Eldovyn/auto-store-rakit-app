from mongoengine import Document, IntField, FloatField


class LiveStockModel(Document):
    guild_id = IntField(required=True)
    channel_id = IntField(required=True)
    message_id = IntField(required=True)
    updated_at = FloatField(required=True)
    meta = {"collection": "live_stock"}
