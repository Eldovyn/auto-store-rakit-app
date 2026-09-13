from .database import Database
from models import PurchaseModel


class Purchase(Database):
    @staticmethod
    async def insert(channel_id):
        if purchase := PurchaseModel.objects().first():
            purchase.channel_id = channel_id
            purchase.save()
            return purchase
        else:
            purchase = PurchaseModel(channel_id=channel_id)
            purchase.save()
            return purchase

    @staticmethod
    async def get(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return PurchaseModel.objects().first()
        elif category == "channel":
            return PurchaseModel.objects(channel_id=channel_id).first()

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        channel_id = kwargs.get("channel_id")
        if category == "channel":
            return PurchaseModel.objects(channel_id=channel_id).delete()
        elif category == "guild":
            return PurchaseModel.objects.delete()
