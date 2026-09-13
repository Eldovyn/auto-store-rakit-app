import nextcord
from nextcord.ext import commands
from nextcord import Webhook
import yaml
import aiohttp
from databases import Reputation as ReputationDatabase
import re


class OnReputation(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            return
        if not message.channel.id == self.data["channel_reputation"]:
            return
        embed = message.embeds[0]
        if not embed:
            return
        webhook_url = self.data["webhook_reputation"]
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(webhook_url, session=session)
            if webhook:
                message_result = await webhook.fetch_message(message.id)
                description = embed.description
                match = re.search(r"^.{6}(.{1})", description) if description else None
                result_id = match.group(1) if match else None
                if not result_id:
                    return
                if not result_id.isdigit():
                    return
                result_id = int(result_id)
                if not (
                    data_rep := await ReputationDatabase().get(
                        "reputation_id", reputation_id=result_id
                    )
                ):
                    return
                await ReputationDatabase().update(
                    "add_message_id_bot",
                    reputation_id=result_id,
                    message_id_bot=message_result.id,
                )


def setup(bot):
    bot.add_cog(OnReputation(bot))
