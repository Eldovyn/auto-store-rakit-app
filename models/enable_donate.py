from mongoengine import (
    Document,
    BooleanField,
)


class EnableDonateModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_donate"}
