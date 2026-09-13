import nextcord
from nextcord.ext import commands
import re
from databases import (
    ChannelDonate as ChannelDonateDatabase,
    Player as PlayerDatabase,
    Leaderboard as LeaderboardDatabase,
    EnableDonate as EnableDonateDatabase,
)
import yaml


class OnDonateLock(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (status := await EnableDonateDatabase().get("guild")) and not status.status:
            return
        if not message.guild:
            return
        if not message.author.bot:
            return
        if not (ch := await ChannelDonateDatabase().get()):
            return
        if not message.channel.id == ch.lock:
            return
        if not message.embeds:
            return
        embed = message.embeds[0]
        description = embed.description
        if not description:
            return
        print(description)
        growid_match = re.search(r"GrowID\s*:\s*([\w\d]+)", description)
        growid = growid_match.group(1) if growid_match else None

        amount_match = re.search(r"Amount\s*:\s*(\d+)", description)
        amount = amount_match.group(1) if amount_match else None
        try:
            amount = int(amount)
        except:
            return
        if not growid or not amount:
            return
        if not (user := await PlayerDatabase().get("growid", growid=growid)):
            return await message.reply(
                "you are not registered. please set your growid first"
            )
        world_lock = 0
        if "World Lock" in description or "World Locks" in description:
            world_lock += amount
        elif "Diamond Lock" in description:
            world_lock += amount * 100
        elif "Blue Gem Lock" in description:
            world_lock += amount * 100 * 100
        result_balance = await PlayerDatabase().update(
            "discord_id",
            discord_id=user.discord_id,
            amount=user.world_lock + world_lock,
            updated_at=nextcord.utils.utcnow().timestamp(),
        )
        result_growid = None
        if not result_balance.growid == growid:
            result_growid = await PlayerDatabase().update(
                "growid",
                new_growid=growid,
                updated_at=nextcord.utils.utcnow().timestamp(),
                discord_id=user.discord_id,
            )
        await message.reply(
            f"""Successfully Adding `{world_lock} world lock` To `{user.growid if not result_growid else result_growid.growid}` ({nextcord.utils.get(message.guild.members, id=user.discord_id).mention})
Your Balance Is `{result_balance.world_lock} world lock`"""
        )
        await LeaderboardDatabase().update(
            "player",
            updated_at=nextcord.utils.utcnow().timestamp(),
        )


def setup(bot):
    bot.add_cog(OnDonateLock(bot))
