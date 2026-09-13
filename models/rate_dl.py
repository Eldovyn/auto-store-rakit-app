from mongoengine import Document, IntField, FloatField


class RateDLModel(Document):
    rate = IntField(required=True)
    updated_at = FloatField(required=True)
    meta = {"collection": "rate_dl"}
