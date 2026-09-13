import nextcord
from nextcord.ext import commands, tasks
from databases import (
    Player as PlayerDatabase,
    Leaderboard as LeaderboardDatabase,
    ModeLiveStockDatabase,
)
from ui import DropdownLiveEmbed, ButtonLiveEmbed
from databases import Maintenance as MaintenanceDatabase
from utils import GenerateEmbeds
import yaml
import traceback


class OnLeaderboard(commands.Cog):
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
                view = (
                    DropdownLiveEmbed(self.bot)
                    if mode_live_stock.mode == "dropdown"
                    else ButtonLiveEmbed(self.bot)
                )
            else:
                view = (
                    DropdownLiveEmbed(self.bot)
                    if self.data_content["mode"] == "dropdown"
                    else ButtonLiveEmbed(self.bot)
                )

            if (mt := await MaintenanceDatabase().get("all")) and mt[0].status:
                if mode_live_stock.mode == "dropdown":
                    await view.disable_dropdown()
                else:
                    await view.disable_buttons()

            if not (data := await LeaderboardDatabase().get("guild")):
                return

            guild = self.bot.get_guild(data.guild_id)
            if not guild:
                return

            channel = guild.get_channel(data.channel_id)
            if not channel:
                return

            try:
                message = await channel.fetch_message(data.message_id)
            except Exception as e:
                return

            if leaderboard := await PlayerDatabase().get("leaderboard"):
                embed = await GenerateEmbeds().generate_leaderboard(
                    leaderboard[: self.data_content["leaderboard_embed"]],
                    guild,
                    OnLeaderboard.data_content["thumbnail"],
                )
                await message.edit(embed=embed, view=view)
            else:
                embed = await GenerateEmbeds().generate_leaderboard(
                    [], guild, OnLeaderboard.data_content["thumbnail"]
                )
                await message.edit(embed=embed, view=view)

        except Exception:
            traceback.print_exc()

    @check_current_task.before_loop
    async def before_check_current_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(OnLeaderboard(bot))
