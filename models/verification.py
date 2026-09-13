from mongoengine import Document, IntField


class VerificationModel(Document):
    role_id = IntField(required=True)
    channel_id = IntField(required=True)
    message_id = IntField(required=True)
    meta = {"collection": "verification"}
