import nextcord
from nextcord.ext import commands
from databases import (
    ChannelDonate as ChannelDonateDatabase,
    Player as PlayerDatabase,
    Leaderboard as LeaderboardDatabase,
    RateDL as RateDlDatabase,
    EnableSaweria as EnableSaweriaDatabase,
)
import re
from utils import Misc
import yaml


class OnDonateSociabuzz(commands.Cog):
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
        if not message.channel.id == ch.sociabuzz:
            return
        if not message.embeds:
            return
        if not (rate_dl := await RateDlDatabase().get()):
            return await message.reply("mention admin to set rate diamond lock")
        embed = message.embeds[0]
        description = embed.title
        if not description:
            return
        amount_match = re.search(r"\d{1,3}(,\d{3})*", description)
        name_match = re.search(r"from\s+(\w+)", description)

        amount = amount_match.group() if amount_match else None
        name = name_match.group(1) if name_match else None

        if not name or not rupiah:
            return

        try:
            rupiah = int(amount.replace(",", ""))
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
    bot.add_cog(OnDonateSociabuzz(bot))
