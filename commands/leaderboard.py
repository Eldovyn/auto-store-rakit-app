import nextcord
from nextcord.ext import commands, application_checks
import yaml
from utils import CustomCheck, DataNotFound, Misc, InteractionResponse
from databases import (
    Player as PlayerDatabase,
)
from ui import Paginated as PaginatedView


class Leaderboard(commands.Cog):
    from utils.config import data

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="to show leaderboard player")
    @application_checks.check(CustomCheck().check_maintenance)
    async def leaderboard(
        self,
        interaction: nextcord.Interaction,
        per_page: int = nextcord.SlashOption(
            description="number of items per page",
            required=False,
            min_value=1,
            default=2,
        ),
    ):
        await InteractionResponse.response_loading(interaction)
        if not (product := await PlayerDatabase().get("leaderboard")):
            raise DataNotFound("leaderboard", interaction.guild_id)
        paginated_arr = await Misc.split_array(product, per_page)

        embeds = []
        for idx, page in enumerate(paginated_arr):
            embed = (
                nextcord.Embed(
                    title=f"Leaderboard",
                    color=nextcord.Color.green(),
                )
                .set_image(self.data["thumbnail"])
                .set_thumbnail(interaction.guild.icon.url)
                .set_footer(text=f"{interaction.guild.name}")
            )
            for i, value in enumerate(page):
                balance = f"{await Misc.format_price(0)}"
                if value.world_lock > 0:
                    balance = f"{await Misc.format_price(value.world_lock)}"
                embed.add_field(
                    name=f"""{self.data['emoji_crown']} {value.growid} {self.data['emoji_crown']}""",
                    value=f"""{self.data['emoji_arrow']} Total Buy : {value.total_buy}
{self.data['emoji_arrow']} World Lock : {balance}
{f'{self.data["emoji_line"] * 6}' if i == 9 else ''}""",
                    inline=False,
                )
            embeds.append(embed)

        if embeds:
            view = PaginatedView(embeds)
            await view.disable_buttons()
            await interaction.edit_original_message(
                embed=embeds[0],
                view=view,
            )


def setup(bot):
    bot.add_cog(Leaderboard(bot))
