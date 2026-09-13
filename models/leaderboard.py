from mongoengine import Document, IntField, FloatField


class LeaderboardModel(Document):
    guild_id = IntField(required=True)
    channel_id = IntField(required=True)
    message_id = IntField(required=True)
    updated_at = FloatField(required=True)
    meta = {"collection": "leaderboard"}
