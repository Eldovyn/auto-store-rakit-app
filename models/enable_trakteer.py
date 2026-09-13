from mongoengine import (
    Document,
    BooleanField,
)


class EnableTrakteerModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_trakteer"}
