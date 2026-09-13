from nextcord.ext import commands
import yaml
import sys
import nextcord


class OnReady(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        from ui import (
            Verification as VerificationView,
            GrowID as GrowIDView,
            QrisPayment,
        )

        self.bot.add_view(VerificationView())
        self.bot.add_view(GrowIDView(self.bot))
        self.bot.add_view(QrisPayment(self.bot))
        await self.bot.change_presence(
            status=nextcord.Status.dnd,
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching,
                name="Nexblu Store",
            ),
        )
        print(f"bot is online as {self.bot.user}")
        print(f'successfully connected to {self.data["mongodb_url"]}')


def setup(bot):
    bot.add_cog(OnReady(bot))
