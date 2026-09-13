from models import PlayerModel, ReputationModel
from utils import DataNotFound


class Reputation:
    @staticmethod
    async def insert(reputation_id, message, star, created_at, image, discord_id):
        try:
            user = PlayerModel.objects.get(discord_id=discord_id)
        except:
            raise DataNotFound("player", data=discord_id)
        reputation = ReputationModel(
            reputation_id=reputation_id,
            message=message,
            star=star,
            created_at=created_at,
            image=image,
            player=user,
        )
        reputation.save()
        return reputation

    @staticmethod
    async def update(category, **kwargs):
        message_id_user = kwargs.get("message_id_user")
        message_id_bot = kwargs.get("message_id_bot")
        reputation_id = kwargs.get("reputation_id")
        if category == "add_message_id_bot":
            if rep := ReputationModel.objects(reputation_id=reputation_id).first():
                rep.message_id_bot = message_id_bot
                rep.save()
                return rep
        elif category == "add_message_id_user":
            if rep := ReputationModel.objects(reputation_id=reputation_id).first():
                rep.message_id_user = message_id_user
                rep.save()
                return rep

    @staticmethod
    async def delete(category, **kwargs):
        reputation_id = kwargs.get("reputation_id")
        if category == "guild":
            return ReputationModel.objects.delete()
        elif category == "reputation_id":
            return ReputationModel.objects(reputation_id=reputation_id).delete()

    @staticmethod
    async def get(category, **kwargs):
        reputation_id = kwargs.get("reputation_id")
        if category == "guild":
            return list(ReputationModel.objects.all())
        elif category == "reputation_id":
            return ReputationModel.objects(reputation_id=reputation_id).first()
