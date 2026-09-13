from mongoengine import Document, IntField


class ReputationChannelModel(Document):
    channel_id = IntField(required=True)
    meta = {"collection": "reputation_channel"}
