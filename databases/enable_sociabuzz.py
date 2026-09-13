from models import EnableSociabuzzModel
from .database import Database


class EnableSociabuzz(Database):
    @staticmethod
    async def insert():
        if not (data := EnableSociabuzzModel.objects.first()):
            enable = EnableSociabuzzModel(status=False)
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
            return EnableSociabuzzModel.objects().first()
