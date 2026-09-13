from mongoengine import Document, IntField, ReferenceField, CASCADE, FloatField
from .product import ProductModel


class BuyGetModel(Document):
    min_buy = IntField(required=True)
    get_product = IntField(required=True)
    promotion_end = FloatField(required=True)
    product = ReferenceField(ProductModel, required=True, reverse_delete_rule=CASCADE)
    meta = {"collection": "buy_get"}
