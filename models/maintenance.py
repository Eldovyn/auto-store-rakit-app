from mongoengine import Document, FloatField, BooleanField


class MaintenanceModel(Document):
    created_at = FloatField(required=True)
    status = BooleanField(required=True)
    meta = {"collection": "maintenance"}
