from models import LeaderboardModel


class Leaderboard:
    @staticmethod
    async def insert(guild_id, message_id, channel_id, updated_at):
        if lb := LeaderboardModel.objects(guild_id=guild_id).first():
            lb.channel_id = channel_id
            lb.message_id = message_id
            lb.save()
            return lb
        else:
            leaderboard = LeaderboardModel(
                guild_id=guild_id,
                message_id=message_id,
                channel_id=channel_id,
                updated_at=updated_at,
            )
            leaderboard.save()
            return leaderboard

    @staticmethod
    async def update(category, **kwargs):
        updated_at = kwargs.get("updated_at")
        if category == "player":
            if lb := LeaderboardModel.objects().first():
                lb.updated_at = updated_at
                lb.save()
                return lb

    @staticmethod
    async def delete(category, **kwargs):
        message_id = kwargs.get("message_id")
        if category == "message_id":
            return LeaderboardModel.objects(message_id=message_id).delete()
        elif category == "guild":
            return LeaderboardModel.objects.delete()

    @staticmethod
    async def get(category, **kwargs):
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if category == "guild":
            return LeaderboardModel.objects().first()
        elif category == "message_id":
            return LeaderboardModel.objects(message_id=message_id).first()
        elif category == "channel_id":
            return LeaderboardModel.objects(channel_id=channel_id).first()
