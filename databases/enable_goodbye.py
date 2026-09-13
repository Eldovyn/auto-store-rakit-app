from models import EnableGoodbyeModel
from .database import Database


class EnableGoodbye(Database):
    @staticmethod
    async def insert():
        if not (data := EnableGoodbyeModel.objects.first()):
            enable = EnableGoodbyeModel(status=False)
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
            return EnableGoodbyeModel.objects().first()
