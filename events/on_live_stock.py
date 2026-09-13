import nextcord
from nextcord.ext import commands, tasks
from databases import (
    LiveStock as LiveStockDatabase,
    Product as ProductDatabase,
    ModeLiveStockDatabase,
)
from ui import ButtonLiveEmbed, DropdownLiveEmbed
from databases import Maintenance as MaintenanceDatabase
from utils import GenerateEmbeds
import yaml
import re
import traceback


class OnLiveStock(commands.Cog):
    from utils.config import data as data_content

    def __init__(self, bot):
        self.bot = bot
        self.loop_task = self.check_current_task.start()

    def cog_unload(self):
        self.loop_task.cancel()

    @tasks.loop(seconds=15)
    async def check_current_task(self):
        try:
            if mode_live_stock := await ModeLiveStockDatabase().get("guild"):
                if mode_live_stock.mode == "dropdown":
                    view = DropdownLiveEmbed(self.bot)
                else:
                    view = ButtonLiveEmbed(self.bot)
            else:
                if self.data_content["mode"] == "dropdown":
                    view = DropdownLiveEmbed(self.bot)
                else:
                    view = ButtonLiveEmbed(self.bot)
            if (mt := await MaintenanceDatabase().get("all")) and mt[0].status:
                if mode_live_stock.mode == "dropdown":
                    await view.disable_dropdown()
                else:
                    await view.disable_buttons()
            if not (data := await LiveStockDatabase().get("guild")):
                return
            guild = self.bot.get_guild(data.guild_id)
            channel = guild.get_channel(data.channel_id)
            message = await channel.fetch_message(data.message_id)
            status = None
            try:
                channel_donation_status = guild.get_channel(
                    self.data_content["channel_id_status"]
                )
                message_donation = await channel_donation_status.fetch_message(
                    self.data_content["message_id_status"]
                )
            except:
                pass
            else:
                if message_donation.embeds:
                    embed = message_donation.embeds[0]
                    description = embed.description
                    if description:
                        pattern = r"Status\s*:\s*(\w+)"
                        match = re.search(pattern, description) if description else None
                        status = match.group(1) if match else None
            stats_embed = await GenerateEmbeds().generate_stats(
                guild, OnLiveStock.data_content["thumbnail"], status
            )
            if product := await ProductDatabase().get("all"):
                embed = await GenerateEmbeds().generate_live_stock(
                    product[: self.data_content["live_stock_embed"]],
                    guild,
                    OnLiveStock.data_content["thumbnail"],
                )
                await message.edit(embeds=[stats_embed, embed], view=view)
            else:
                embed = await GenerateEmbeds().generate_live_stock(
                    [],
                    guild,
                    OnLiveStock.data_content["thumbnail"],
                )
                await message.edit(embeds=[stats_embed, embed], view=view)
        except:
            traceback.print_exc()

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnLiveStock(bot))
