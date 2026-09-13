from mongoengine import (
    Document,
    BooleanField,
)


class EnableGoodbyeModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_goodbye"}
