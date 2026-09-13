from models import GoodbyeModel
from .database import Database


class Goodbye(Database):
    @staticmethod
    async def insert(
        channel_id,
    ):
        if channel := GoodbyeModel.objects().first():
            channel.channel_id = channel_id
            channel.save()
            return channel
        else:
            result = GoodbyeModel(channel_id=channel_id)
            result.save()
            return result

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return GoodbyeModel.objects().first().delete()
        elif category == "channel":
            return GoodbyeModel.objects(channel_id=channel_id).first().delete()

    @staticmethod
    async def get(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return GoodbyeModel.objects().first()
        elif category == "channel":
            return GoodbyeModel.objects(channel_id=channel_id).first()
