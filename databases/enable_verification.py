from models import EnableVerificationModel
from .database import Database


class EnableVerification(Database):
    @staticmethod
    async def insert():
        if not (data := EnableVerificationModel.objects.first()):
            enable = EnableVerificationModel(status=False)
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
            return EnableVerificationModel.objects().first()
