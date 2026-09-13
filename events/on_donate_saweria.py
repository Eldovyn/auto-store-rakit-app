import nextcord
from nextcord.ext import commands
from databases import ChannelDonate as ChannelDonateDatabase
import re
from databases import (
    Player as PlayerDatabase,
    Leaderboard as LeaderboardDatabase,
    RateDL as RateDlDatabase,
    EnableSaweria as EnableSaweriaDatabase,
)
import yaml
from utils import Misc


class OnDonateSaweria(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (status := await EnableSaweriaDatabase().get("guild")) and not status.status:
            return
        if not message.guild:
            return
        if not message.author.bot:
            return
        if not (ch := await ChannelDonateDatabase().get()):
            return
        if not message.channel.id == ch.saweria:
            return
        if not message.embeds:
            return
        if not (rate_dl := await RateDlDatabase().get()):
            return await message.reply("mention admin to set rate diamond lock")
        embed = message.embeds[0]
        description = embed.title
        if not description:
            return
        matches = re.search(r"(\d+\.\d+)\s+from\s+(\w+)", description)
        number = matches.group(1) if matches else None
        name = matches.group(2) if matches else None
        if not name or not rupiah:
            return
        try:
            rupiah = int(number.replace(".", ""))
        except:
            return

        if not (user := await PlayerDatabase().get("growid", growid=name)):
            return await message.reply(
                "you are not registered. please set your growid first"
            )

        world_lock = await Misc().calculate_rate_dl(rate_dl.rate, rupiah)

        result_balance = await PlayerDatabase().update(
            "discord_id",
            discord_id=user.discord_id,
            amount=user.world_lock + world_lock,
            updated_at=nextcord.utils.utcnow().timestamp(),
        )
        await message.reply(
            f"""Successfully Adding `{world_lock} world lock` To `{user.growid}` ({nextcord.utils.get(message.guild.members, id=user.discord_id).mention})
Your Balance Is `{result_balance.world_lock} world lock`"""
        )
        await LeaderboardDatabase().update(
            "player",
            updated_at=nextcord.utils.utcnow().timestamp(),
        )


def setup(bot):
    bot.add_cog(OnDonateSaweria(bot))
