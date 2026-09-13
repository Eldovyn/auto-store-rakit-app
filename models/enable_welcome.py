from mongoengine import (
    Document,
    BooleanField,
)


class EnableWelcomeModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_welcome"}
