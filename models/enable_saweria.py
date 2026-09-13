from mongoengine import (
    Document,
    BooleanField,
)


class EnableSaweriaModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_saweria"}
