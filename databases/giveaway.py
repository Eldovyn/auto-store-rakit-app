from models import GiveawayModel
from .database import Database


class Giveaway(Database):
    @staticmethod
    async def insert(
        guild_id,
        channel_id,
        message_id,
        role_id,
        hoster_id,
        item,
        file_name,
        created_at,
        giveaway_end,
        description,
    ):
        giveaway = GiveawayModel(
            guild_id=guild_id,
            channel_id=channel_id,
            message_id=message_id,
            role_id=role_id,
            hoster_id=hoster_id,
            item=item,
            file_name=file_name,
            created_at=created_at,
            giveaway_end=giveaway_end,
            description=description,
        )
        giveaway.save()
        return giveaway

    @staticmethod
    async def update(category, **kwargs):
        pass

    @staticmethod
    async def delete(category, **kwargs):
        created_at = kwargs.get("created_at")
        if category == "created_at":
            return GiveawayModel.objects(created_at=created_at).delete()
        elif category == "guild":
            return GiveawayModel.objects.delete()

    @staticmethod
    async def get(category, **kwargs):
        created_at = kwargs.get("created_at")
        if category == "guild":
            return list(GiveawayModel.objects().all())
        elif category == "created_at":
            return GiveawayModel.objects(created_at=created_at).first()
