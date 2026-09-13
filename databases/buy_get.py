from models import BuyGetModel, ProductModel
from .database import Database
from utils import DataNotFound, DuplicateData
from mongoengine.errors import NotUniqueError


class BuyGet(Database):
    @staticmethod
    async def insert(code, min_buy, get_product, promotion_end):
        if prod := ProductModel.objects(code=code).first():
            try:
                buyget = BuyGetModel(
                    min_buy=min_buy,
                    get_product=get_product,
                    product=prod,
                    promotion_end=promotion_end,
                )
                buyget.save()
            except NotUniqueError:
                raise DuplicateData("buy_get", code)
            return buyget
        raise DataNotFound("product", code)

    @staticmethod
    async def update(category, **kwargs):
        code = kwargs.get("code")
        min_buy = kwargs.get("min_buy")
        get_product = kwargs.get("get_product")
        if category == "product":
            if prod := ProductModel.objects(code=code).first():
                if not (buy_get := BuyGetModel.objects(product=prod).first()):
                    raise DataNotFound("buy-get", code)
                buy_get.min_buy = min_buy
                buy_get.get_product = get_product
                buy_get.save()
                return buy_get

    @staticmethod
    async def delete(category, **kwargs):
        code = kwargs.get("code")
        if category == "guild":
            return BuyGetModel.objects.delete()
        elif category == "product":
            if prod := ProductModel.objects(code=code).first():
                return BuyGetModel.objects(product=prod).delete()

    @staticmethod
    async def get(category, **kwargs):
        code = kwargs.get("code")
        if category == "code":
            if prod := ProductModel.objects(code=code).first():
                return BuyGetModel.objects(product=prod).first()
        elif category == "guild":
            return list(BuyGetModel.objects.all())
