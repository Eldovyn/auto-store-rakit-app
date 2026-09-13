import nextcord
from nextcord.ext import commands
from databases import (
    QrisChannel as QrisChannelDatabase,
    RateDL as RateDlDatabase,
    Player as PlayerDatabase,
    Leaderboard as LeaderboardDatabase,
)
import re
from utils import Misc, QrisPayment


class OnQris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            return
        if not message.embeds:
            return
        if not (ch := await QrisChannelDatabase().get("guild")):
            return
        if not message.channel.id == ch.channel_id:
            return
        if not (rate_dl := await RateDlDatabase().get()):
            return await message.reply("mention admin to set rate diamond lock")
        embed = message.embeds[0]
        if not (description := embed.description):
            return
        status_match = (
            re.search(r"Status\s*:\s*([^\n]+)", description) if description else None
        )
        amount = (
            re.search(r"Amount\s*:\s*([^\n]+)", description) if description else None
        )
        user = re.search(r"User\s*:\s*<@!?(\d+)>", description) if description else None

        status = status_match.group(1) if status_match else None
        amount = amount.group(1) if amount else None
        user = user.group(1) if user else None

        if not status or not amount or not user:
            return

        parse_rupiah = await QrisPayment().parse_rupiah(amount)
        if status != "Paid":
            return
        player = await PlayerDatabase().get("discord_id", discord_id=int(user))
        if not player:
            return await message.reply(
                "you are not registered. please set your growid first"
            )
        if not parse_rupiah:
            return
        created_at = nextcord.utils.utcnow().timestamp()
        world_lock = await Misc().calculate_rate_dl(rate_dl.rate, parse_rupiah)
        result_balance = await PlayerDatabase().update(
            "discord_id",
            discord_id=player.discord_id,
            amount=player.world_lock + world_lock,
            updated_at=created_at,
        )
        await message.reply(
            f"""Successfully Adding `{world_lock} world lock` To `{result_balance.growid}` ({nextcord.utils.get(message.guild.members, id=result_balance.discord_id).mention})
Your Balance Is `{result_balance.world_lock} world lock`"""
        )
        await LeaderboardDatabase().update(
            "player",
            updated_at=created_at,
        )


def setup(bot):
    bot.add_cog(OnQris(bot))
