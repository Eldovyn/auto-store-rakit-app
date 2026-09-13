from mongoengine import Document, StringField, IntField


class ProductModel(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    code = StringField(required=True, unique=True)
    role = IntField(required=True)
    category = StringField(required=True)
    min_buy = IntField(required=True)
    price = IntField(required=False)
    meta = {"collection": "product"}
