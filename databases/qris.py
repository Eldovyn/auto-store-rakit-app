from .database import Database
from models import PlayerModel, QrisModel
from utils import DataNotFound


class Qris(Database):
    @staticmethod
    async def insert(discord_id, unique_code, amount, created_at):
        if player := PlayerModel.objects(discord_id=discord_id).first():
            qris = QrisModel(
                player=player,
                unique_code=unique_code,
                amount=amount,
                created_at=created_at,
            )
            qris.save()
            return qris
        raise DataNotFound("player", discord_id)

    @staticmethod
    async def get(category, **kwargs):
        messsage_id = kwargs.get("message_id")
        unique_code = kwargs.get("unique_code")
        discord_id = kwargs.get("discord_id")
        if category == "message_id":
            return QrisModel.objects(message_id=messsage_id).first()
        elif category == "all":
            return list(QrisModel.objects.all())
        elif category == "unique_code":
            return QrisModel.objects(unique_code=unique_code).first()
        elif category == "discord_id":
            if player := PlayerModel.objects(discord_id=discord_id).first():
                if qris := QrisModel.objects(player=player).first():
                    return qris

    @staticmethod
    async def update(category, **kwargs):
        message_id = kwargs.get("message_id")
        unique_code = kwargs.get("unique_code")
        if category == "message_id":
            if data := QrisModel.objects(unique_code=unique_code).first():
                data.message_id = message_id
                data.save()
                return data

    @staticmethod
    async def delete(category, **kwargs):
        message_id = kwargs.get("message_id")
        unique_code = kwargs.get("unique_code")
        if category == "message_id":
            return QrisModel.objects(message_id=message_id).delete()
        elif category == "unique_code":
            return QrisModel.objects(unique_code=unique_code).delete()
