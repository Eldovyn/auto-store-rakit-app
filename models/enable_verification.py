from mongoengine import (
    Document,
    BooleanField,
)


class EnableVerificationModel(Document):
    status = BooleanField(required=True)
    meta = {"collection": "enable_verification"}
