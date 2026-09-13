from mongoengine import (
    Document,
    DynamicField,
    ReferenceField,
    FloatField,
    StringField,
    CASCADE,
)
from .product import ProductModel


class StockModel(Document):
    file_name = StringField(required=False)
    item = DynamicField(required=True)
    created_at = FloatField(required=True)
    product = ReferenceField(ProductModel, required=True, reverse_delete_rule=CASCADE)
    meta = {"collection": "stock"}
