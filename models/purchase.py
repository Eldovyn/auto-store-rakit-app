from mongoengine import Document, IntField


class PurchaseModel(Document):
    channel_id = IntField(required=True)
    meta = {"collection": "purchase"}
