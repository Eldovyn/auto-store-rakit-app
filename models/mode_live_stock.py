from mongoengine import Document, StringField


class ModeLiveStockModel(Document):
    mode = StringField(required=True)
    meta = {"collection": "mode_live_stock"}
