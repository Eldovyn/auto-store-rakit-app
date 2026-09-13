from mongoengine import (
    Document,
    IntField,
)


class ChannelDonateModel(Document):
    lock = IntField(required=True)
    saweria = IntField(required=True)
    trakteer = IntField(required=True)
    sociabuzz = IntField(required=True)
    transfer = IntField(required=True)
    meta = {"collection": "channel_donate"}
