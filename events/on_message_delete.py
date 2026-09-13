import nextcord
from nextcord.ext import commands
from databases import (
    Verification as VerificationDatabase,
    LiveStock as LiveStockDatabase,
    Leaderboard as LeaderboardDatabase,
)


class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if verif := await VerificationDatabase().get(
            "message_id", message_id=message.id
        ):
            await VerificationDatabase().delete("message_id", message_id=message.id)
        if ls := await LiveStockDatabase().get("message_id", message_id=message.id):
            await LiveStockDatabase().delete("message_id", message_id=message.id)
        if lb := await LeaderboardDatabase().get("message_id", message_id=message.id):
            await LeaderboardDatabase().delete("message_id", message_id=message.id)


def setup(bot):
    bot.add_cog(OnMessageDelete(bot))
