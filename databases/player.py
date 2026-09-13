from models import PlayerModel
from utils import DataNotFound, DuplicateData


class Player:
    @staticmethod
    async def insert(discord_id, growid, created_at, updated_at):
        if player := PlayerModel.objects(growid__iexact=growid).first():
            if player.discord_id != discord_id:
                raise DuplicateData("growid", growid)
        if player_discord_id := PlayerModel.objects(discord_id=discord_id).first():
            if player_discord_id.growid.lower() == growid.lower():
                raise DuplicateData("growid", growid)
            player_discord_id.growid = growid
            player_discord_id.updated_at = updated_at
            player_discord_id.save()
            return player_discord_id
        player = PlayerModel(
            discord_id=discord_id,
            growid=growid,
            created_at=created_at,
            updated_at=updated_at,
        )
        player.save()
        return player

    @staticmethod
    async def delete(category, **kwargs):
        discord_id = kwargs.get("discord_id")
        if category == "discord_id":
            return PlayerModel.objects(discord_id=discord_id).delete()
        elif category == "guild":
            return PlayerModel.objects.delete()

    @staticmethod
    async def get(category, **kwargs):
        discord_id = kwargs.get("discord_id")
        growid = kwargs.get("growid")
        if category == "discord_id":
            return PlayerModel.objects(discord_id=discord_id).first()
        elif category == "growid":
            return PlayerModel.objects(growid__iexact=growid).first()
        elif category == "all":
            return list(PlayerModel.objects.all())
        elif category == "leaderboard":
            return list(
                PlayerModel.objects.all().order_by(
                    "-total_buy",
                    "-world_lock",
                    "created_at",
                    "updated_at",
                )
            )

    @staticmethod
    async def update(category, **kwargs):
        discord_id = kwargs.get("discord_id")
        updated_at = kwargs.get("updated_at")
        amount = kwargs.get("amount")
        total_buy = kwargs.get("total_buy")
        new_growid = kwargs.get("new_growid")
        if category == "discord_id":
            if player := PlayerModel.objects(discord_id=discord_id).first():
                player.updated_at = updated_at
                player.world_lock = amount
                player.save()
                return player
            raise DataNotFound("player", discord_id)
        elif category == "total_buy":
            if player := PlayerModel.objects(discord_id=discord_id).first():
                player.total_buy = total_buy
                player.updated_at = updated_at
                player.save()
                return player
            raise DataNotFound("player", discord_id)
        elif category == "total_world_lock":
            if player := PlayerModel.objects(discord_id=discord_id).first():
                player.total_world_lock = amount
                player.updated_at = updated_at
                player.save()
                return player
            raise DataNotFound("player", discord_id)
        elif category == "growid":
            if player := PlayerModel.objects(discord_id=discord_id).first():
                player.growid = new_growid
                player.updated_at = updated_at
                player.save()
                return player
