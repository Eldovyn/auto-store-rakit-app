from mongoengine import (
    Document,
    BooleanField,
)


class EnableQrisModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_qris"}
