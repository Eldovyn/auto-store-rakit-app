from mongoengine import Document, IntField


class GoodbyeModel(Document):
    channel_id = IntField(required=True)
    meta = {"collection": "goodbye"}
