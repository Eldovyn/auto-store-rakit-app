from .database import Database
from models import ModeLiveStockModel


class ModeLiveStockDatabase(Database):
    @staticmethod
    async def insert(mode):
        if live_stock := ModeLiveStockModel.objects().first():
            live_stock.mode = mode
            live_stock.save()
            return live_stock
        else:
            live_stock = ModeLiveStockModel(mode=mode)
            live_stock.save()
            return live_stock

    @staticmethod
    async def get(category, **kwargs):
        if category == "guild":
            return ModeLiveStockModel.objects().first()

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        pass
