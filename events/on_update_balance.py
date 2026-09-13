import nextcord
from nextcord.ext import commands
import re
from databases import (
    Player as PlayerDatabase,
    ChannelDonate as ChannelDonateDatabase,
    Leaderboard as LeaderboardDatabase,
    EnableTransfer as EnableTransferDatabase,
)
import yaml


class OnUpdateBalance(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            status := await EnableTransferDatabase().get("guild")
        ) and not status.status:
            return
        if not message.guild:
            return
        if not message.author.bot:
            return
        if not (ch := await ChannelDonateDatabase().get()):
            return
        if not message.channel.id == ch.transfer:
            return
        if not message.embeds:
            return
        embed = message.embeds[0]
        description = embed.description
        if not description:
            return
        user_id_match = re.search(r"<@!?(\d+)>", description)
        amount_match = re.search(r"Amount\s*:\s*`([+-]?\d+)`", description)
        growid_match = re.search(r"GrowID\s*:\s*`([\w\d]+)`", description)

        growid = growid_match.group(1) if growid_match else None
        amount = amount_match.group(1) if amount_match else None
        user_id = user_id_match.group(1) if user_id_match else None
        try:
            user_id = int(user_id)
        except:
            return
        if not user_id or not amount or not growid:
            return
        if not (user := await PlayerDatabase().get("growid", growid=growid)):
            return await message.reply(
                "you are not registered. please set your growid first"
            )
        if amount.startswith("+"):
            category = "add"
        elif amount.startswith("-"):
            category = "sub"
        else:
            category = "replace"
        await message.reply(
            f"""successfully {category} balance `{amount} world lock` to `{growid}` ({(nextcord.utils.get(message.guild.members, id=int(user_id))).mention})
Your Balance Is `{user.world_lock} world lock`"""
        )
        await LeaderboardDatabase().update(
            "player",
            updated_at=nextcord.utils.utcnow().timestamp(),
        )


def setup(bot):
    bot.add_cog(OnUpdateBalance(bot))
