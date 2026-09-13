from .database import Database
from models import ReputationChannelModel


class ReputationChannel(Database):
    @staticmethod
    async def insert(channel_id):
        if purchase := ReputationChannelModel.objects().first():
            purchase.channel_id = channel_id
            purchase.save()
            return purchase
        else:
            purchase = ReputationChannelModel(channel_id=channel_id)
            purchase.save()
            return purchase

    @staticmethod
    async def get(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return ReputationChannelModel.objects().first()
        elif category == "channel":
            return ReputationChannelModel.objects(channel_id=channel_id).first()

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "channel":
            return ReputationChannelModel.objects(channel_id=channel_id).delete()
        elif category == "guild":
            return ReputationChannelModel.objects.delete()
