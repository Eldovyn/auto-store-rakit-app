from .database import Database
from models import QrisChannelModel


class QrisChannel(Database):
    @staticmethod
    async def insert(guild_id, channel_id):
        if purchase := QrisChannelModel.objects().first():
            purchase.guild_id = guild_id
            purchase.channel_id = channel_id
            purchase.save()
            return purchase
        else:
            purchase = QrisChannelModel(guild_id=guild_id, channel_id=channel_id)
            purchase.save()
            return purchase

    @staticmethod
    async def get(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return QrisChannelModel.objects().first()
        elif category == "channel":
            return QrisChannelModel.objects(channel_id=channel_id).first()

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "channel":
            return QrisChannelModel.objects(channel_id=channel_id).delete()
        elif category == "guild":
            return QrisChannelModel.objects.delete()
