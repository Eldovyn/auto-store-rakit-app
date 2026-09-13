import nextcord
from nextcord.ext import commands, tasks
from databases import (
    Qris as QrisDatabase,
    QrisChannel as QrisChannelDatabase,
    RateDL as RateDlDatabase,
)
from utils import QrisPayment as QP
import yaml
from utils import Misc
import traceback


class OnQrisPayment(commands.Cog):
    from utils.config import data as data_content

    def __init__(self, bot):
        self.bot = bot
        self.loop_task = self.check_current_task.start()

    def cog_unload(self):
        self.loop_task.cancel()

    @tasks.loop(seconds=10)
    async def check_current_task(self):
        try:
            if not (rdl := await RateDlDatabase().get()):
                return
            if data := await QrisDatabase().get("all"):
                for d in data:
                    if not d.message_id:
                        continue
                    user = await self.bot.fetch_user(d.player.discord_id)
                    dm_channel = await user.create_dm()
                    message = await dm_channel.fetch_message(d.message_id)
                    world_lock = await Misc().calculate_rate_dl(rdl.rate, d.amount)
                    rupiah = await Misc().format_rupiah(d.amount)
                    if not (
                        data_database := await QrisDatabase().get(
                            "message_id", message_id=d.message_id
                        )
                    ):
                        continue
                    status_qris = await QP().check_status(data_database.unique_code)
                    if not message.embeds:
                        continue
                    embed = message.embeds[0]
                    if not status_qris:
                        continue
                    if status_qris and "transaction_status" not in status_qris:
                        continue
                    if status_qris["transaction_status"] == "pending":
                        continue
                    if status_qris["transaction_status"] == "expire":
                        embed.description = f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} World Lock : {world_lock}
{self.data_content['emoji_arrow']} Status : {status_qris["transaction_status"]}"""
                        embed.set_image(url=None)
                        await message.edit(embed=embed, view=None)
                        await QrisDatabase().delete(
                            "message_id", message_id=d.message_id
                        )
                        if ch := await QrisChannelDatabase().get("guild"):
                            channel = await self.bot.fetch_channel(ch.channel_id)
                            if channel:
                                await channel.send(
                                    embed=nextcord.Embed(
                                        title=f"Qris Payment Information",
                                        description=f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Status : Canceled
{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} User : {user.mention}""",
                                        color=nextcord.Color.green(),
                                    ).set_image(self.data_content["thumbnail"]),
                                )
                        continue
                    if status_qris["transaction_status"] == "settlement":
                        embed.description = f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} World Lock : {world_lock} world lock
{self.data_content['emoji_arrow']} Status : {status_qris["transaction_status"]}"""
                        embed.set_image(url=None)
                        await message.edit(embed=embed, view=None)
                        await QrisDatabase().delete(
                            "message_id", message_id=d.message_id
                        )
                        if ch := await QrisChannelDatabase().get("guild"):
                            channel = await self.bot.fetch_channel(ch.channel_id)
                            if channel:
                                await channel.send(
                                    embed=nextcord.Embed(
                                        title=f"Qris Payment Information",
                                        description=f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Status : Paid
{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} User : {user.mention}""",
                                        color=nextcord.Color.green(),
                                    ).set_image(self.data_content["thumbnail"]),
                                )
                        continue
                    if status_qris["transaction_status"] == "cancel":
                        embed.description = f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} World Lock : {world_lock}
{self.data_content['emoji_arrow']} Status : {status_qris["transaction_status"]}"""
                        embed.set_image(url=None)
                        await message.edit(embed=embed, view=None)
                        await QrisDatabase().delete(
                            "message_id", message_id=d.message_id
                        )
                        if ch := await QrisChannelDatabase().get("guild"):
                            channel = await self.bot.fetch_channel(ch.channel_id)
                            if channel:
                                await channel.send(
                                    embed=nextcord.Embed(
                                        title=f"Qris Payment Information",
                                        description=f"""{status_qris['order_id']} <t:{int(data_database.created_at)}:R>

{self.data_content['emoji_arrow']} Status : Canceled
{self.data_content['emoji_arrow']} Amount : {rupiah}
{self.data_content['emoji_arrow']} User : {user.mention}""",
                                        color=nextcord.Color.green(),
                                    ).set_image(self.data_content["thumbnail"]),
                                )
                    continue
        except:
            traceback.print_exc()

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnQrisPayment(bot))
