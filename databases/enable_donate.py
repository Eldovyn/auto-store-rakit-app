from models import EnableDonateModel
from .database import Database


class EnableDonate(Database):
    @staticmethod
    async def insert():
        if not (data := EnableDonateModel.objects.first()):
            enable = EnableDonateModel(status=False)
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
            return EnableDonateModel.objects().first()
