from models import EnableTransferModel
from .database import Database


class EnableTransfer(Database):
    @staticmethod
    async def insert():
        if not (data := EnableTransferModel.objects.first()):
            enable = EnableTransferModel(status=False)
            enable.save()
            return enable
        data.status = not data.status
        data.save()
        return data

    @staticmethod
    async def update(category, **kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def get(category, **kwargs):
        if category == "guild":
            return EnableTransferModel.objects().first()
