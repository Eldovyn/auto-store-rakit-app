from models import EnableTrakteerModel
from .database import Database


class EnableTrakteer(Database):
    @staticmethod
    async def insert():
        if not (data := EnableTrakteerModel.objects.first()):
            enable = EnableTrakteerModel(status=False)
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
            return EnableTrakteerModel.objects().first()
