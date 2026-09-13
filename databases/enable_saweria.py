from models import EnableSaweriaModel
from .database import Database


class EnableSaweria(Database):
    @staticmethod
    async def insert():
        if not (data := EnableSaweriaModel.objects.first()):
            enable = EnableSaweriaModel(status=False)
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
            return EnableSaweriaModel.objects().first()
