from mongoengine import Document, IntField


class WelcomeModel(Document):
    channel_id = IntField(required=True)
    meta = {"collection": "welcome"}
