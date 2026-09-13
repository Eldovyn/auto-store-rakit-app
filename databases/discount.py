from models import DiscountModel, ProductModel
from .database import Database
from utils import DataNotFound, DuplicateData
import traceback
from mongoengine.errors import NotUniqueError


class Discount(Database):
    @staticmethod
    async def insert(code, price, created_at, discount_end):
        if prod := ProductModel.objects(code=code).first():
            try:
                discount = DiscountModel(
                    price=price,
                    created_at=created_at,
                    discount_end=discount_end,
                    product=prod,
                )
                discount.save()
                return discount
            except NotUniqueError:
                raise DuplicateData("discount", code)
        raise DataNotFound("product", code)

    @staticmethod
    async def update(category, **kwargs):
        price = kwargs.get("price")
        code = kwargs.get("code")
        duration = kwargs.get("duration")
        if category == "discount":
            if prod := ProductModel.objects(code=code).first():
                if not (disc := DiscountModel.objects(product=prod).first()):
                    raise DataNotFound("discount", code)
                disc.price = price
                disc.save()
                return disc
        elif category == "discount-duration":
            if prod := ProductModel.objects(code=code).first():
                if not (disc := DiscountModel.objects(product=prod).first()):
                    raise DataNotFound("discount", code)
                disc.price = price
                disc.discount_end = duration
                disc.save()
                return disc

    @staticmethod
    async def delete(category, **kwargs):
        code = kwargs.get("code")
        if category == "product":
            if prod := ProductModel.objects(code=code).first():
                if disc := DiscountModel.objects(product=prod).first():
                    disc.delete()
                    return True
                raise DataNotFound("discount", code)
            raise DataNotFound("product", code)
        elif category == "guild":
            return DiscountModel.objects().first().delete()

    @staticmethod
    async def get(category, **kwargs):
        code = kwargs.get("code")
        if category == "product":
            if prod := ProductModel.objects(code=code).first():
                return DiscountModel.objects(product=prod).first()
            return None
        elif category == "guild":
            return DiscountModel.objects().all()
