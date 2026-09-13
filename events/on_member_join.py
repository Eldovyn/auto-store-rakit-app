import nextcord
from nextcord.ext import commands
from databases import Welcome as WelcomeDatabase, EnableWelcome as EnableWelcomeDatabase
import yaml


class OnMemberJoin(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if (status := await EnableWelcomeDatabase().get("guild")) and not status.status:
            return
        if member.guild.id not in self.data["guild_id"]:
            return
        if not (ch := await WelcomeDatabase().get("guild")):
            return
        if not (channel := self.bot.get_channel(ch.channel_id)):
            return
        await channel.send(
            embed=nextcord.Embed(
                title=f"Welcome To {member.guild.name}",
                description=f"**Hey {member.mention}, Welcome To My Server**",
                color=nextcord.Color.green(),
            )
            .set_footer(text=f"{member.guild.name}")
            .set_image(self.data["thumbnail"])
        )


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
