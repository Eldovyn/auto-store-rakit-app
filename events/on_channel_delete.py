import nextcord
from nextcord.ext import commands
from databases import (
    Verification as VerificationDatabase,
    LiveStock as LiveStockDatabase,
    Leaderboard as LeaderboardDatabase,
)


class OnChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if verif := await VerificationDatabase().get(
            "channel_id", channel_id=channel.id
        ):
            await VerificationDatabase().delete("channel", channel_id=channel.id)
        if ls := await LiveStockDatabase().get("channel_id", channel_id=channel.id):
            await LiveStockDatabase().delete("channel", channel_id=channel.id)
        if lb := await LeaderboardDatabase().get("channel_id", channel_id=channel.id):
            await LeaderboardDatabase().delete("channel", channel_id=channel.id)


def setup(bot):
    bot.add_cog(OnChannelDelete(bot))
