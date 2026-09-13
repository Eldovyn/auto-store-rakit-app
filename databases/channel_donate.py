from models import ChannelDonateModel
from .database import Database


class ChannelDonate(Database):
    @staticmethod
    async def insert(
        lock,
        saweria,
        trakteer,
        sociabuzz,
        transfer,
    ):
        if channel := ChannelDonateModel.objects().first():
            channel.lock = lock
            channel.saweria = saweria
            channel.trakteer = trakteer
            channel.sociabuzz = sociabuzz
            channel.transfer = transfer
            channel.save()
            return channel
        else:
            result = ChannelDonateModel(
                lock=lock,
                saweria=saweria,
                trakteer=trakteer,
                sociabuzz=sociabuzz,
                transfer=transfer,
            )
            result.save()
            return result

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        if category == "guild":
            return ChannelDonateModel.objects().first().delete()

    @staticmethod
    async def get():
        return ChannelDonateModel.objects().first()
