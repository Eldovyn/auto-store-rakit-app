from .database import Database
from models import VerificationModel


class Verification(Database):
    @staticmethod
    async def insert(role_id, channel_id, message_id):
        if verif := VerificationModel.objects().first():
            verif.channel_id = channel_id
            verif.message_id = message_id
            verif.role_id = role_id
            verif.save()
            return verif
        else:
            v = VerificationModel(
                role_id=role_id, message_id=message_id, channel_id=channel_id
            )
            v.save()
            return v

    @staticmethod
    async def get(category, **kwargs):
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return VerificationModel.objects().first()
        elif category == "message_id":
            return VerificationModel.objects(message_id=message_id).first()
        elif category == "channel_id":
            return VerificationModel.objects(channel_id=channel_id).first()

    @staticmethod
    async def update(**kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if category == "message_id":
            return VerificationModel.objects(message_id=message_id).delete()
        elif category == "guild":
            return VerificationModel.objects.delete()
        elif category == "channel":
            return VerificationModel.objects(channel_id=channel_id).delete()
