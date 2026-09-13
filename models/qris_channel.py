from mongoengine import Document, IntField


class QrisChannelModel(Document):
    guild_id = IntField(required=True)
    channel_id = IntField(required=True)
    meta = {"collection": "qris_channel"}
