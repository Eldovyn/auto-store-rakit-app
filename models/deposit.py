from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField


class GrowtopiaModel(EmbeddedDocument):
    world = StringField(required=True)
    owner = StringField(required=True)
    bot = StringField(required=True)


class DepositModel(Document):
    growtopia = EmbeddedDocumentField(GrowtopiaModel)
    saweria = StringField(required=False)
    trakteer = StringField(required=False)
    sociabuzz = StringField(required=False)
    meta = {"collection": "deposit"}
