from mongoengine import (
    Document,
    BooleanField,
)


class EnableSociabuzzModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_sociabuzz"}
