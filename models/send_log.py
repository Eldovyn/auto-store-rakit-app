from mongoengine import Document, IntField


class SendLogModel(Document):
    channel_id = IntField(required=True)
    meta = {"collection": "send_log"}
