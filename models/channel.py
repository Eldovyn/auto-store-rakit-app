from mongoengine import Document, IntField


class ChannelModel(Document):
    reputation = IntField(required=True)
    live_stock = IntField(required=True)
    saweria = IntField(required=True)
    trakteer = IntField(required=True)
    sociabuzz = IntField(required=True)
    purchase = IntField(required=True)
    transfer = IntField(required=True)
    welcome = IntField(required=True)
    goodbye = IntField(required=True)
    donate = IntField(required=True)
    leaderboard = IntField(required=True)
    verification = IntField(required=True)
    meta = {"collection": "channel"}
