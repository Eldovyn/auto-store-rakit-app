import nextcord
from nextcord.ext import commands
from databases import Goodbye as GoodbyeDatabase, EnableGoodbye as EnableGoodbyeDatabase
import yaml


class OnMemberRemove(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if (status := await EnableGoodbyeDatabase().get("guild")) and not status.status:
            return
        if member.guild.id not in self.data["guild_id"]:
            return
        if not (ch := await GoodbyeDatabase().get("guild")):
            return
        if not (channel := self.bot.get_channel(ch.channel_id)):
            return
        await channel.send(
            embed=nextcord.Embed(
                title=f"Goodbye To {member.guild.name}",
                description=f"**Hey {member.mention}, Goodbye To My Server**",
                color=nextcord.Color.green(),
            )
            .set_footer(text=f"{member.guild.name}")
            .set_image(self.data["thumbnail"])
        )


def setup(bot):
    bot.add_cog(OnMemberRemove(bot))
