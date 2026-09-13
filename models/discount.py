from mongoengine import (
    Document,
    ReferenceField,
    FloatField,
    CASCADE,
    IntField,
)
from .product import ProductModel


class DiscountModel(Document):
    price = IntField(required=True)
    created_at = FloatField(required=True)
    discount_end = FloatField(required=True)
    product = ReferenceField(
        ProductModel, required=True, reverse_delete_rule=CASCADE, unique=True
    )
    meta = {"collection": "discount"}
