from models import EnableQrisModel
from .database import Database


class EnableQris(Database):
    @staticmethod
    async def insert():
        if not (data := EnableQrisModel.objects.first()):
            enable = EnableQrisModel(status=False)
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
            return EnableQrisModel.objects().first()
