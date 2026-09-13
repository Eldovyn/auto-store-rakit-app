from mongoengine import Document, FloatField, IntField, BinaryField, StringField


class GiveawayModel(Document):
    guild_id = IntField(required=True)
    channel_id = IntField(required=True)
    message_id = IntField(required=True)
    role_id = IntField(required=True)
    hoster_id = IntField(required=True)
    item = BinaryField(required=True)
    file_name = StringField(required=True)
    created_at = FloatField(required=True)
    giveaway_end = FloatField(required=True)
    description = StringField(required=True)
    meta = {"collection": "giveaway"}
