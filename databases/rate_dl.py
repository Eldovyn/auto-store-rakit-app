from models import RateDLModel
from .database import Database


class RateDL(Database):
    @staticmethod
    async def insert(rate, updated_at):
        if dl := RateDLModel.objects().first():
            dl.rate = rate
            dl.updated_at = updated_at
            dl.save()
            return dl
        else:
            result = RateDLModel(rate=rate, updated_at=updated_at)
            result.save()
            return result

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        pass

    @staticmethod
    async def get():
        return RateDLModel.objects().first()
