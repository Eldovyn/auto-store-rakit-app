from mongoengine import (
    Document,
    BooleanField,
)


class EnableTransferModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_transfer"}
