from models import EnableWelcomeModel
from .database import Database


class EnableWelcome(Database):
    @staticmethod
    async def insert():
        if not (data := EnableWelcomeModel.objects.first()):
            enable = EnableWelcomeModel(status=False)
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
            return EnableWelcomeModel.objects().first()
