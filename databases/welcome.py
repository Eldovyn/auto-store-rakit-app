from models import WelcomeModel
from .database import Database


class Welcome(Database):
    @staticmethod
    async def insert(
        channel_id,
    ):
        if channel := WelcomeModel.objects().first():
            channel.channel_id = channel_id
            channel.save()
            return channel
        else:
            result = WelcomeModel(channel_id=channel_id)
            result.save()
            return result

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        if category == "guild":
            return WelcomeModel.objects().first().delete()

    @staticmethod
    async def get(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return WelcomeModel.objects().first()
        elif category == "channel":
            return WelcomeModel.objects(channel_id=channel_id).first()
